"""Blogly application."""
from flask import Flask
from models import connect_db
from routes.Main_Views import main_views
from routes.User_Views import user_views
from routes.Post_Views import post_views
from routes.Tag_Views import tag_views


app = Flask(__name__)
app.config['SECRET_KEY'] = 'a secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
# db.drop_all()
db.create_all()

app.register_blueprint(main_views)
app.register_blueprint(user_views, url_prefix='/users')
app.register_blueprint(tag_views, url_prefix='/tags')
app.register_blueprint(post_views)
