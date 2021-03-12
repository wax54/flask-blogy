from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import User

db = SQLAlchemy()


app = Flask(__name__)
db_name = 'blogly'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///{blogly}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.drop_all()
db.create_all()
