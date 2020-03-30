import os
import random
import time

from flask import Flask, request, render_template, session, \
    flash, redirect, url_for, jsonify
from flask_mail import Mail, Message
from celery import Celery


app = Flask(__name__, instance_relative_config= True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

# mail extension init
mail = Mail(app)

# Celery setup
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


################# Celery Magic Zone ###############

@celery.task
def send_async_email(email_data):
    """Background task to send an email with Flask-Mail."""
    msg = Message(email_data['subject'],
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email_data['to']])
    msg.body = email_data['body']
    with app.app_context():
        mail.send(msg)


@celery.task(bind=True)
def long_task(self):
    """Background task that runs a long 
        function with progress reports.
    """

    verb = ['Reading', 'Retrieving', 'Preparing', 'Mixing', 'Tasting']
    adjective = ['nutritious', 'heavy', 'lean', 'quick', 'neat']
    noun = ['sandwich', 'cupcakes', 'cookies', 'nuts mix', 'biscuits']
    message = ''
    total = random.randint(10, 50)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total,
                                'status': message})
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}

################# Celery tripper(app route) ###############

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', email=session.get('email', ''))
    email = request.form['email']
    session['email'] = email

    # send the email
    email_data = {
        'subject': 'Celery snack-Flask',
        'to': email,
        'body': 'This is a test email sent from a background Celery task.\n\
            regards\n\
            Alex kagai'
    }
    if request.form['submit'] == 'Send':
        # send right away
        send_async_email.delay(email_data)
        flash('Sending email to {0}'.format(email))
    else:
        # send in one minute
        send_async_email.apply_async(args=[email_data], countdown=60)
        flash('An email will be sent to {0} in one minute'.format(email))

    return redirect(url_for('index'))


@app.route('/longtask', methods=['POST'])
def longtask():
    task = long_task.apply_async()
    return jsonify({}), 202, {'Location': url_for('taskstatus',task_id=task.id)}


def res_data(state, current, total, status):
    """Build response data for a task
    """
    return {
            'state': state,
            'current': current,
            'total': total,
            'status': status,
        }


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = res_data(task.state, 0, 1, 'Pending...')
    
    elif task.state != 'FAILURE':
        response = res_data(task.state, task.info.get('current', 0), 
                            task.info.get('total', 1),
                            task.info.get('status', '')
                    )
        
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = res_data(task.state, 1, 1, str(task.info))
        # this is the exception raised
        
    return jsonify(response)


if __name__ == '__main__':
    app.run()
