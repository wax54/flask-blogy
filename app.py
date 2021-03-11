"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

# u = User(first_name="jake", last_name="paulson", image_url="https://www.homepont.com/ehns/pic")

# db.session.add(u)
# db.session.commit()


@app.route('/')
def home_page():
    return redirect('/users')


@app.route('/users')
def list_of_users():
    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route('/users/new')
def new_user_form():
    return render_template('new_user.html')


@app.route('/users/new', methods=["POST"])
def submit_new_user():
    f_name = request.form['first_name']
    l_name = request.form['last_name']
    image = request.form['image_url']
    
    new_user = User(first_name=f_name, last_name=l_name, image_url=image)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/')


@app.route('users/<int:user_id>')
def describe_user(user_id):
    user = User.query.get(user_id)
    return render_template('user_description.html', user=user)



