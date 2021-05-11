import os

SECRET_KEY = os.environ['SECRET_KEY']

# SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
# db_connection_string = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
# SQLALCHEMY_DATABASE_URI = db_connection_string
SQLALCHEMY_TRACK_MODIFICATIONS = False
#SQLALCHEMY_POOL_RECYCLE = 280

# WTForms
WTF_CSRF_TIME_LIMIT = None
WTF_CSRF_CHECK_DEFAULT = True
