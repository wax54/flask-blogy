from models import db, DEFAULT_IMAGE_URL


class PostTag(db.Model):
    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id', ondelete='cascade'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey(
        'tags.id', ondelete='cascade'), primary_key=True)
