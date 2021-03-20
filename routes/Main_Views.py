from flask import Blueprint, render_template, redirect
from models.User import User
from models.Post import Post
from models.Tag import Tag

main_views = Blueprint('main_views', __name__)


@main_views.route('/')
def home_page():
    """Shows the apps home Page"""
    posts = Post.get_last(5)
    return render_template('post_list.html', posts=posts)
    #return redirect('/users')
