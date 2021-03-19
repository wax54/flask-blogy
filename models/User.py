from models import db, DEFAULT_IMAGE_URL, update_db, BasicOperations


class User(db.Model, BasicOperations):
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
