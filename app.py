"""Blogly application."""
from flask import Flask, render_template, request, redirect, flash
from models import db, connect_db, User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'a secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    """Shows the apps home Page"""
    return redirect('/users')


@app.route('/users')
def list_of_users():
    """Shows all the users in the apps db"""
    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route('/users/new')
def new_user_form():
    """shows the form that, when submitted, will create a new user in the DB"""
    return render_template('user_new_form.html')


@app.route('/users/new', methods=["POST"])
def create_user():
    """Attempts to creates a new user in the DB from the passed in POST request data
    Redirects to the all users list if successful """
    f_name = request.form['first_name']
    l_name = request.form['last_name']
    image = request.form['image_url']
    #first name is required
    if f_name == '':
        flash('You must enter a First Name')
        return redirect('/users/new')
    
    new_user = User(first_name=f_name, last_name=l_name)
    new_user.update_image(image)

    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>')
def describe_user(user_id):
    """Displays info about the specified user"""
    user = User.query.get(user_id)
    return render_template('user_description.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """shows the form that, when submitted, will update a user in the DB"""
    user = User.query.get(user_id)
    return render_template('user_edit_form.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def submit_user_edit(user_id):
    """Attepmts to update the info of the user with an id of user_id.
    uses the passed in POST request data
    Redirects to the describe user if successful """
    #if theres no first name, we can't take it
    f_name = request.form['first_name']
    if f_name == '':
        flash('You must enter a First Name')
        return redirect(f'/users/{user_id}/edit')
    
    # get the user from the table
    user = User.query.get(user_id)
    # update the user info from the form
    user.first_name = f_name
    user.last_name = request.form['last_name']
    user.update_image(request.form['image_url'])

    db.session.add(user)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/users')
