"""Blogly application."""
from flask import Flask, render_template, request, redirect, flash
from models import db, connect_db, User, Post, Tag, update_tags


app = Flask(__name__)
app.config['SECRET_KEY'] = 'a secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
# db.drop_all()
# db.create_all()


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
    # first name is required
    if f_name == '':
        flash('You must enter a First Name')
        return redirect('/users/new')
    else:
        User.add(f_name, l_name, image)
        return redirect('/users')


@app.route('/users/<int:user_id>')
def describe_user(user_id):
    """Displays info about the specified user"""
    user = User.get(user_id)
    return render_template('user_details.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """shows the form that, when submitted, will update a user in the DB"""
    user = User.get(user_id)
    return render_template('user_edit_form.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
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
        User.update_by_id(user_id, f_name, l_name, image)
        return redirect(f'/users/{user_id}')


@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Deletes the specified user from the DB"""
    User.delete_by_id(user_id)
    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """Shows the New Post Form"""
    user = User.get(user_id)
    tags = Tag.get_all()
    return render_template('post_new_form.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def new_post_submission(user_id):
    """Submits the new post to the DB"""
    post_dict = process_post_form(request.form)

    if post_dict['title']:
        title = post_dict['title']
        content = post_dict['content']
        post = Post.add(title, content, user_id)

        tags = post_dict['tags']
        update_tags(post.id, tags)

        return redirect(f'/users/{user_id}')
    else:
        flash('Your Post Must Have a Title and Content!')
        return redirect(f'/users/{user_id}/posts/new')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Displays info about the specified post"""
    post = Post.get(post_id)

    return render_template('post_details.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """Displays the form to edit the specified post"""
    post = Post.get(post_id)
    tags = Tag.get_all()
    return render_template('post_edit_form.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post_submission(post_id):
    """updates the specified post to use the newly submitted data"""

    post_dict = process_post_form(request.form)

    if post_dict['title']:
        title = post_dict['title']
        content = post_dict['content']
        tags = post_dict['tags']

        Post.update_by_id(post_id, title, content, tags)
        return redirect(f'/posts/{post_id}')
    else:
        flash('Your Post Must Have a Title and Content!')
        return redirect(f'/posts/{post_id}/edit')


@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Deletes the specified post from the DB"""
    post = Post.delete_by_id(post_id)
    return redirect('/')


@app.route('/tags')
def list_tags():
    """Lists all the tags"""
    tags = Tag.query.all()
    return render_template('tag_list.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def describe_tags(tag_id):
    """Lists the posts assosiated with the tag"""
    tag = Tag.get(tag_id)
    return render_template('tag_details.html', tag=tag)


@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    """deletes the specified tag"""
    Tag.delete_by_id(tag_id)
    return redirect('/tags')


@app.route('/tags/new')
def new_tag_form():
    """displays the form to add a new tag"""
    return render_template('tag_new_form.html')


@app.route('/tags/new', methods=["POST"])
def new_tag_submission():
    """Submits the new tag to the DB"""
    name = request.form['name']
    if name == '':
        flash('Your tag must have a name!')
        return redirect(f'/tags/new')
    else:
        try:
            Tag.add(name)
            return redirect(f'/tags')
        except:
            flash('I think We already got that Tag!')
            return redirect(f'/tags/new')


@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    """displays the form to edit the tag"""
    return render_template("tag_edit_form.html", tag=Tag.get(tag_id))


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag_submission(tag_id):
    """Process edit form, edit tag, and redirects to the tags list."""

    tag = Tag.get(tag_id)
    new_name = request.form.get('name')
    if not new_name:
        flash('Your tag must have a name!')
        return redirect(f'/tags/{tag_id}/edit')
    else:
        try:
            tag.update_name(new_name)
            return redirect(f'/tags')
        except:
            flash("That um.. didnt work...")
            return redirect(f'/tags/{tag_id}/edit')


def process_post_form(form):
    title = form.get('title').strip()
    content = form.get('content').strip()

    if not title or not content:
        return False
    else:
        post = {'title': title, 'content': content}
        all_tags = Tag.get_all()
        post_tags = []
        for tag in all_tags:
            if form.get(f'tag_{tag.id}') == 'on':
                post_tags.append(tag.id)
        post['tags'] = post_tags
        return post
