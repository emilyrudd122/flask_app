import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'qwerty.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATETIME_FORMAT = "%d-%m-%Y %H:%M"
    PATIENTS_PER_PAGE = 5
    CALENDAR_ID = "d6b6kgf2fhrkesmotonnu3i6vg@group.calendar.google.com"