from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@54.254.104.240/name_of_db'
db = SQLAlchemy(app)

from app import views, models