# Imports:
from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from helpers import split_skills


# Configurations:
APP_ROOT = path.dirname(path.abspath(__file__)) # app root = projects path
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/vasilis/pycourses.db' # sqlite db url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '\xc9!Zi\xab\x8b\xae}D`\x17\xc69\x81\xcd\x93\xec+\xf1\xf2s&DG'
# from os import urandom
# app.config['SECRET_KEY'] = urandom(24) => urandom() generates a 32 length random secret key
app.jinja_env.filters['split_skills'] = split_skills # add custom filter in jinja-2
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB maximum bytes


db = SQLAlchemy(app)
from views import *


# Database and server set up:
if __name__ == '__main__':
   db.create_all()
   app.run(debug=True)
