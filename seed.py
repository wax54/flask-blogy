from models import db, User, Post
from app import app

db.drop_all()
db.create_all()


users = [
    User(first_name='Carl', last_name='Boulder'),
    User(first_name='Brenda', last_name='Baker'),
    User(first_name='Susan', last_name='Rice',
         image_url='www.mycustomimage.com'),
    User(first_name='Oba', last_name='Zelous')
]

posts = [
    Post(title='Snax', content='content goes here', user_id=1),
    Post(title='Built', content='somewhere else', user_id=2),
    Post(title='Super', content='blasted shredz', user_id=1),
    Post(title='Obsurd', content='Major Content Right Here', user_id=3),
    Post(title='Blanket Statments', content='''Things are bad
    Things are good
    Dont believe me? 
    Super star''', user_id=2)
]

db.session.add_all(users)
db.session.commit()

db.session.add_all(posts)
db.session.commit()
