import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', default='sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='123456789')
    PEOPLE_FOLDER = os.path.join('app/static', 'people_photo')
    FLASK_ADMIN_SWATCH = 'superhero'
    ADMIN_NAME = os.getenv('ADMIN_NAME', default='superhero')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', default='superhero')
