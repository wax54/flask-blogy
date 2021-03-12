from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import User


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db_name = 'test_blogly'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///{db_name}'

db = SQLAlchemy()

db.app = app
db.init_app(app)

db.drop_all()
db.create_all()
