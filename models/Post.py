from models import db, DEFAULT_IMAGE_URL, update_db, BasicOperations
from models.PostTag import PostTag


class Post (db.Model, BasicOperations):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           server_default=db.func.statement_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete="cascade"))

    def update_tags(self, new_tags):
        post_id = self.id
        current_tags = db.session.query(
            PostTag.tag_id).filter_by(post_id=post_id).all()
        curr_tags = [tag[0] for tag in current_tags]

        tags_to_add = set(new_tags) - set(curr_tags)
        tags_to_remove = set(curr_tags) - set(new_tags)
        for tag_id in tags_to_add:
            post_tag = PostTag(post_id=post_id, tag_id=tag_id)
            db.session.add(post_tag)
        for tag_id in tags_to_remove:
            PostTag.query.filter_by(post_id=post_id, tag_id=tag_id).delete()
        db.session.commit()

    @classmethod
    def add(cls, title, content, user_id):
        new_post = cls(title=title, content=content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        return new_post

    @classmethod
    def update_by_id(cls, post_id, title, content, tags):
        # get the post from the table
        post = cls.get(post_id)
        # update the post info from the form
        post.title = title
        post.content = content
        post.update_tags(tags)
        update_db(post)
        return post
