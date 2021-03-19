from flask import Blueprint, render_template, request, redirect, flash
from models.User import User

user_views = Blueprint('user_views', __name__)


@user_views.route('')
def list_of_users():
    """Shows all the users in the apps db"""
    users = User.query.all()
    return render_template('user_list.html', users=users)


@user_views.route('/new')
def new_user_form():
    """shows the form that, when submitted, will create a new user in the DB"""
    return render_template('user_new_form.html')


@user_views.route('/new', methods=["POST"])
def create_user():
    """Attempts to creates a new user in the DB from the passed in POST request data
    Redirects to the all users list if successful """
    f_name = request.form['first_name']
    l_name = request.form['last_name']
    image = request.form['image_url']
    # first name is required
    if f_name == '':
        flash('You must enter a First Name')
        return redirect('/users/new')
    else:
        User.add(f_name, l_name, image)
        return redirect('/users')


@user_views.route('/<int:user_id>')
def describe_user(user_id):
    """Displays info about the specified user"""
    user = User.get(user_id)
    return render_template('user_details.html', user=user)


@user_views.route('/<int:user_id>/edit')
def edit_user_form(user_id):
    """shows the form that, when submitted, will update a user in the DB"""
    user = User.get(user_id)
    return render_template('user_edit_form.html', user=user)


@user_views.route('/<int:user_id>/edit', methods=["POST"])
def submit_user_edit(user_id):
    """Attepmts to update the info of the user with an id of user_id.
    uses the passed in POST request data
    Redirects to the describe user if successful """
    # if theres no first name, we can't take it
    f_name = request.form.get('first_name')
    l_name = request.form.get('last_name')
    image = request.form.get('image_url')

    if not f_name:
        flash('You must enter a First Name')
        return redirect(f'/users/{user_id}/edit')
    else:
        # maybe it would make more sense to get the user and then put an update user
        # on the instance

        User.update_by_id(user_id, f_name, l_name, image)
        return redirect(f'/users/{user_id}')


@user_views.route('/<int:user_id>/delete')
def delete_user(user_id):
    """Deletes the specified user from the DB"""
    User.delete_by_id(user_id)
    return redirect('/users')
