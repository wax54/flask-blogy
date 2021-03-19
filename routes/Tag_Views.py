from flask import Blueprint, render_template, request, redirect, flash
from models import User, Tag, Post

tag_views = Blueprint('tag_views', __name__)


@tag_views.route('/')
def list_tags():
    """Lists all the tags"""
    tags = Tag.query.all()
    return render_template('tag_list.html', tags=tags)


@tag_views.route('/<int:tag_id>')
def describe_tags(tag_id):
    """Lists the posts assosiated with the tag"""
    tag = Tag.get(tag_id)
    return render_template('tag_details.html', tag=tag)


@tag_views.route('/<int:tag_id>/delete')
def delete_tag(tag_id):
    """deletes the specified tag"""
    Tag.delete_by_id(tag_id)
    return redirect('/tags')


@tag_views.route('/new')
def new_tag_form():
    """displays the form to add a new tag"""
    return render_template('tag_new_form.html')


@tag_views.route('/new', methods=["POST"])
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


@tag_views.route('/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    """displays the form to edit the tag"""
    return render_template("tag_edit_form.html", tag=Tag.get(tag_id))


@tag_views.route('/<int:tag_id>/edit', methods=["POST"])
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
