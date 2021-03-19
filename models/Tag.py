from models import db, DEFAULT_IMAGE_URL, BasicOperations
from models.Post import Post
from models.PostTag import PostTag


class Tag(db.Model, BasicOperations):
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
    def update_by_id(cls, tag_id, new_name):
        # get the tag from the table
        tag = cls.get(tag_id)
        # update the tag info from the form
        tag.name = name
        update_db(tag)
        return tag
