"""Blogly application."""
from flask import Flask, render_template, request, redirect, flash
from models import db, connect_db, User, Post


app = Flask(__name__)
app.config['SECRET_KEY'] = 'a secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.drop_all()
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
    return render_template('user_details.html', user=user)


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
    """Deletes the specified user from the DB"""
    user = User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """Shows the New Post Form"""
    user = User.query.get_or_404(user_id)
    return render_template('post_new_form.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def new_post_submission(user_id):
    """Submits the new post to the DB"""
    title = request.form['title']
    content = request.form['content']

    if title == '' or content == '':
        flash('Your Post Must Have a Title and Content!')
        return redirect(f'/users/{user_id}/posts/new')
    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Displays info about the specified post"""
    post = Post.query.get_or_404(post_id)
    return render_template('post_details.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """Displays the form to edit the specified post"""
    post = Post.query.get_or_404(post_id)
    return render_template('post_edit_form.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post_submission(post_id):
    """updates the specified post to use the newly submitted data"""
    title = request.form['title']
    content = request.form['content']

    if title == '' or content == '':
        flash('Your Post Must Have a Title and Content!')
        return redirect(f'/posts/{post_id}/edit')
    post = Post.query.get_or_404(post_id)
    post.title = title
    post.content = content

    db.session.add(post)
    db.session.commit()
    return redirect(f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Deletes the specified post from the DB"""
    post = Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect('/')





