import os

from flask import Flask, request, render_template, session, \
    flash, redirect, url_for
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


if __name__ == '__main__':
    app.run()
