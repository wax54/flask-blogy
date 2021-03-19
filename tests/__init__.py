from app import app
from models import db, connect_db

app.config['TESTING'] = True
app.config['SQLALCHEMY_ECHO'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'

connect_db(app)
db.drop_all()
db.create_all()


def get_html_from(path):
    with app.test_client() as client:
        res = client.get(path, follow_redirects=True)
        return res.get_data(as_text=True)
