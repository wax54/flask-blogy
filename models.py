"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

DEFAULT_IMAGE_URL = "/static/default_user_img.jpg"

db = SQLAlchemy()


def connect_db(app):
    """Initiates a connection to the DB"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """ represents the users table in postgressql"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.TEXT, nullable=False)
    last_name = db.Column(db.TEXT, nullable=True)
    image_url = db.Column(db.TEXT, nullable=True)

    

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
