from flask import Blueprint, render_template, request, redirect, flash
from models.User import User
from models.Post import Post
from models.Tag import Tag


post_views = Blueprint('post_views', __name__)


@post_views.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """Shows the New Post Form"""
    user = User.get(user_id)
    tags = Tag.get_all()
    return render_template('post_new_form.html', user=user, tags=tags)


@post_views.route('/users/<int:user_id>/posts/new', methods=["POST"])
def new_post_submission(user_id):
    """Submits the new post to the DB"""
    post_dict = process_post_form(request.form)

    if post_dict['title']:
        title = post_dict['title']
        content = post_dict['content']
        post = Post.add(title, content, user_id)

        tags = post_dict['tags']
        post.update_tags(tags)

        return redirect(f'/users/{user_id}')
    else:
        flash('Your Post Must Have a Title and Content!')
        return redirect(f'/users/{user_id}/posts/new')


@post_views.route('/posts/<int:post_id>')
def show_post(post_id):
    """Displays info about the specified post"""
    post = Post.get(post_id)

    return render_template('post_details.html', post=post)


@post_views.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """Displays the form to edit the specified post"""
    post = Post.get(post_id)
    tags = Tag.get_all()
    return render_template('post_edit_form.html', post=post, tags=tags)


@post_views.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post_submission(post_id):
    """updates the specified post to use the newly submitted data"""

    post_dict = process_post_form(request.form)

    if post_dict:
        title = post_dict['title']
        content = post_dict['content']
        tags = post_dict['tags']

        Post.update_by_id(post_id, title, content, tags)
        return redirect(f'/posts/{post_id}')
    else:
        flash('Your Post Must Have a Title and Content!')
        return redirect(f'/posts/{post_id}/edit')


@post_views.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Deletes the specified post from the DB"""
    post = Post.delete_by_id(post_id)
    return redirect('/')


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
