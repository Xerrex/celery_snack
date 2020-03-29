import os


###### celery configs
CELERY_BROKER_URL= os.environ.get('CELERY_BROKER_URL') or 'redis://0.0.0.0:6379/0'
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://0.0.0.0:6379/0'

##### flask mail configs
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_DEFAULT_SENDER = 'xerrex@github.io'

###################### configs moved to the instance config #########################
# SECRET_KEY = os.envirom.get('SECRET_KEY')
# MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
# MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
