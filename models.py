"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

DEFAULT_IMAGE_URL = "/static/default_user_img.jpg"

db = SQLAlchemy()


def connect_db(app):
    """Initiates a connection to the DB"""
    db.app = app
    db.init_app(app)




class User(db.Model):
    """Represents a row in the users table in postgressql"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.TEXT, nullable=False)
    last_name = db.Column(db.TEXT, nullable=True)
    image_url = db.Column(db.TEXT, nullable=True, default=DEFAULT_IMAGE_URL)
    posts = db.relationship('Post', backref='creator')

    def full_name(self):
        """returns the full name of a user"""
        return f"{self.first_name} {self.last_name}"

    def update_image(self, image):
        """updates the image URL of the user. If none, uses the DEFAULT_IMAGE_URL"""
        if image:
            self.image_url = image
            return True
        else:
            self.image_url = DEFAULT_IMAGE_URL
            return True

    @classmethod
    def add(cls, first_name, last_name=None, image_url=None):
        # if last name is falsey, make it n
        if not last_name:
            last_name = None

        new_user = cls(first_name=first_name, last_name=last_name)
        new_user.update_image(image_url)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def update_by_id(cls, user_id, first_name, last_name=None, image_url=None):
        # get the user from the table
        user = User.get(user_id)
        # update the user info from the form
        user.first_name = first_name
        user.last_name = last_name
        user.update_image(image_url)
        update_db(user)
        return user

    @classmethod
    def delete_by_id(cls, user_id):
        cls.query.filter_by(id=user_id).delete()
        db.session.commit()

    @classmethod
    def get(cls, u_id):
        return cls.query.get_or_404(u_id)


class Post (db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           server_default=db.func.statement_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete="cascade"))

    @classmethod
    def add(cls, title, content, user_id):
        new_post = cls(title=title, content=content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        return new_post

    @classmethod
    def get(cls, p_id):
        return cls.query.get_or_404(p_id)

    @classmethod
    def update_by_id(cls, post_id, title, content):
        # get the post from the table
        post = cls.get(post_id)
        # update the post info from the form
        post.title = title
        post.content = content
        update_db(post)
        return post

    @classmethod
    def delete_by_id(cls, post_id):
        cls.query.filter_by(id=post_id).delete()
        db.session.commit()


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    posts = db.relationship("Post", secondary="posts_tags", backref="tags")

    def update_name(self, val):
        self.name = val
        update_db(self)

    @classmethod
    def add(cls, name):
        new_tag = cls(name=name)
        db.session.add(new_tag)
        db.session.commit()
        return new_tag

    @classmethod
    def get(cls, tag_id):
        return cls.query.get_or_404(tag_id)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def update_by_id(cls, tag_id, new_name):
        # get the tag from the table
        tag = cls.get(tag_id)
        # update the tag info from the form
        tag.name = name
        update_db(tag)
        return tag

    @classmethod
    def delete_by_id(cls, tag_id):
        cls.query.filter_by(id=tag_id).delete()
        db.session.commit()


class PostTag(db.Model):
    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


def update_db(db_obj):
    db.session.add(db_obj)
    db.session.commit()
