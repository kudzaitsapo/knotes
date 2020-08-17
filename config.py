import os


basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'models', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'someverysecuresecretkeythatisencryptedgoeshere'
    UPLOADS_FOLDER = os.path.join(basedir, 'static', 'images', 'uploads')
    ADMIN_PORTAL = os.environ.get('ADMIN_PORTAL') or 'admin'