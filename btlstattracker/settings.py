import os

# Application settings
APP_NAME = 'app'
APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"

# Flask settings
CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = os.environ['WTF_CSRF_SECRET_KEY']

# Flask-Security settings
SECURITY_REGISTERABLE = True
SECURITY_REGISTER_URL = '/register'
SECURITY_REGISTER_USER_TEMPLATE = 'security/register_user.html'
SECURITY_LOGIN_URL = '/login'
SECURITY_LOGIN_USER_TEMPLATE = 'security/login_user.html'
SECURITY_PASSWORD_HASH = os.environ['SECURITY_PASSWORD_HASH']
SECURITY_PASSWORD_SALT = os.environ['SECURITY_PASSWORD_SALT']
SECURITY_SEND_REGISTER_EMAIL = False
#EMAIL_SUBJECT_REGISTER = 'BLAH'