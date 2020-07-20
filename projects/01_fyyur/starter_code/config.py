import os , flask_sqlalchemy
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO_DONE IMPLEMENT DATABASE URL
##using unix domain sockets , refrence : https://stackoverflow.com/questions/23839656/sqlalchemy-no-password-supplied-error
SQLALCHEMY_DATABASE_URI =  'postgresql:///fyyurapp'
SQLALCHEMY_TRACK_MODIFICATIONS = False
