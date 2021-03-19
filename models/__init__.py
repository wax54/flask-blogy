"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

DEFAULT_IMAGE_URL = "/static/default_user_img.jpg"

db = SQLAlchemy()


def connect_db(app):
    """Initiates a connection to the DB"""
    db.app = app
    db.init_app(app)


def update_db(db_obj):
    db.session.add(db_obj)
    db.session.commit()


class BasicOperations():
    @classmethod
    def delete_by_id(cls, user_id):
        cls.query.filter_by(id=user_id).delete()
        db.session.commit()

    @classmethod
    def get(cls, u_id):
        return cls.query.get_or_404(u_id)

    @classmethod
    def get_all(cls):
        return cls.query.all()
