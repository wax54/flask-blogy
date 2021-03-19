from unittest import TestCase
from models import db, connect_db, User, DEFAULT_IMAGE_URL, Post
from app import app

app.config['TESTING'] = True
app.config['SQLALCHEMY_ECHO'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'

connect_db(app)
db.drop_all()
db.create_all()


class UserListRouteTests(TestCase):
    def setUp(self):
        add_user_to_db('Sam', 'Crewe-Sullam')

    def tearDown(self):
        db.drop_all()
        db.create_all()

    def test_returns_user(self):
        html = get_html_from('/users')
        self.assertIn('Sam Crewe-Sullam', html)

    def test_updates_on_multi_user_addition(self):
        html = get_html_from('/users')

        self.assertIn('Sam Crewe-Sullam', html)

        self.assertNotIn('Bagsy GoMeister', html)
        self.assertNotIn('Juliard O Rorik', html)

        add_user_to_db('Bagsy', 'GoMeister')
        add_user_to_db('Juliard', 'O Rorik')

        html = get_html_from('/users')
        self.assertIn('Bagsy GoMeister', html)
        self.assertIn('Juliard O Rorik', html)


class NewUserRouteTests(TestCase):
    def tearDown(self):
        db.drop_all()
        db.create_all()

    def test_get_route_returns_correct_page(self):
        self.assertIn('<h1>CREATE A USER</h1>', get_html_from('/users/new'))

    def test_post_route_redirects_to_user_list(self):
        with app.test_client() as client:
            res = client.post('/users/new',
                              data={'first_name': 'John',
                                    'last_name': 'Doe', 'image_url': 'hello'})
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, 'http://localhost/users')

    def test_post_route_adds_user(self):
        with app.test_client() as client:
            users = User.query.filter_by(
                first_name='John', last_name='Doe').all()
            # user doesn't exist yet
            self.assertEqual(users, [])

            res = client.post('/users/new',
                              data={'first_name': 'John',
                                    'last_name': 'Doe', 'image_url': 'hello'},
                              follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('John Doe', res.get_data(as_text=True))
            user = User.query.filter_by(
                first_name='John', last_name='Doe').one_or_none()
            self.assertEqual(user.image_url, 'hello')

    def test_post_route_gives_an_image_if_one_was_not_provided(self):
        with app.test_client() as client:
            res = client.post('/users/new',
                              data={'first_name': 'John',
                                    'last_name': 'Doe', 'image_url': ''},
                              follow_redirects=True)
            user = User.query.filter_by(
                first_name='John', last_name='Doe').one_or_none()

            self.assertNotEqual(user.image_url, '')
            self.assertEqual(user.image_url, DEFAULT_IMAGE_URL)

    def test_post_route_rejects_no_first_name(self):
        with app.test_client() as client:
            res = client.post('/users/new',
                              data={'first_name': '',
                                    'last_name': 'Doe', 'image_url': ''},
                              follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            user = User.query.filter_by(last_name="doe").one_or_none()
            # user was never made
            self.assertIsNone(user)


class EditUserTests(TestCase):
    def setUp(self):
        self.sam_id = add_user_to_db('Sam', 'Crewe-Sullam')
        self.benny_id = add_user_to_db('Benny', 'G')
        self.toni_id = add_user_to_db(
            'Toni', '', 'https://mysite.com/myimg.jpg')

    def tearDown(self):
        db.drop_all()
        db.create_all()

    def test_get_route_returns_correct_page(self):
        html = get_html_from(f'/users/{self.sam_id}/edit')
        self.assertIn('<h1>EDIT USER!</h1>', html)

    def test_post_route_redirects_to_user_description_page(self):
        with app.test_client() as client:
            res = client.post(f'/users/{self.sam_id}/edit',
                              data={'first_name': 'John',
                                    'last_name': 'Doe', 'image_url': 'hello'})
            self.assertEqual(res.status_code, 302)
            self.assertEqual(
                res.location, f'http://localhost/users/{self.sam_id}')
            res = client.get(res.location)
            html = res.get_data(as_text=True)
            self.assertIn('John Doe', html)

    def test_post_route_edits_user_info(self):
        with app.test_client() as client:
            benny = User.query.get(self.benny_id)
            self.assertEqual(benny.last_name, 'G')
            res = client.post(f'/users/{self.benny_id}/edit',
                              data={'first_name': 'Benny',
                                    'last_name': 'Gee', 'image_url': ''},
                              follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            benny = User.query.get(self.benny_id)
            self.assertEqual(benny.last_name, 'Gee')

    def test_post_route_gives_an_image_if_one_was_not_provided(self):
        with app.test_client() as client:
            toni = User.query.get(self.toni_id)
            self.assertEqual(toni.image_url,
                             'https://mysite.com/myimg.jpg')

            res = client.post(f'/users/{self.toni_id}/edit',
                              data={'first_name': 'Toni',
                                    'last_name': '', 'image_url': ''},
                              follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            toni = User.query.get(self.toni_id)
            self.assertNotEqual(toni.image_url, 'https://mysite.com/myimg.jpg')
            self.assertNotEqual(toni.image_url, '')
            self.assertEqual(toni.image_url, DEFAULT_IMAGE_URL)

    def test_post_route_rejects_no_first_name(self):
        with app.test_client() as client:

            res = client.post(f'/users/{self.sam_id}/edit',
                              data={'first_name': '',
                                    'last_name': 'Doe', 'image_url': ''},
                              follow_redirects=True)
            self.assertEqual(res.status_code, 200)

            sam = User.query.get(self.sam_id)
            self.assertNotEqual(sam.first_name, '')
            # No change was made
            self.assertEqual(sam.first_name, 'Sam')


class DeleteUserTests(TestCase):
    def setUp(self):
        self.sam_id = add_user_to_db('Sam', 'Crewe-Sullam')
        self.benny_id = add_user_to_db('Benny', 'G')
        self.toni_id = add_user_to_db(
            'Toni', '', 'https://mysite.com/myimg.jpg')

    def tearDown(self):
        db.drop_all()
        db.create_all()

    def test_route_deletes_user(self):
        with app.test_client() as client:
            res = client.get(
                f'/users/{self.benny_id}/delete', follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            benny = User.query.get(self.benny_id)
            self.assertIsNone(benny)

    def test_post_route_redirects_to_user_list(self):
        with app.test_client() as client:
            res = client.get(f'/users/{self.sam_id}/delete')

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, 'http://localhost/users')
            res = client.get(res.location)
            html = res.get_data(as_text=True)
            self.assertNotIn('Sam Crewe-Sullam', html)


class EditPostTests(TestCase):
    def setUp(self):
        u_id = add_user_to_db('Sam', 'Crewe-Sullam')
        self.p1_id = add_post_to_db('SuperCool', 'This is content', u_id)
        self.p2_id = add_post_to_db(
            'Major Post Here', 'misleading Titles are the worst', u_id)

    def tearDown(self):
        db.drop_all()
        db.create_all()

    def test_route_edit_form_contains_post_info(self):
        with app.test_client() as client:
            res = client.get(f'/posts/{self.p1_id}/edit')
            html = res.get_data(as_text=True)
            p1 = Post.query.get(self.p1_id)

            self.assertIn(f'value="{p1.title}"', html)
            self.assertIn(f'value="{p1.content}"', html)
            self.assertIn(p1.creator.first_name, html)

    def test_route_returns_404_if_no_post(self):
        with app.test_client() as client:
            res = client.get(f'/posts/10/edit')
            self.assertEqual(res.status_code, 404)


    def test_post_route_edits_post_info(self):
        with app.test_client() as client:
            post = Post.query.get(self.p1_id)
            self.assertEqual(post.title, 'SuperCool')
            res = client.post(f'/posts/{self.p1_id}/edit',
                            data={'title': 'A Different Title',
                                    'content': 'Different Content'},
                            follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            post = Post.query.get(self.p1_id)
            self.assertEqual(post.title, 'A Different Title')
            self.assertEqual(post.content, 'Different Content')

class ViewPostTests(TestCase):
    def setUp(self):
        u_id = add_user_to_db('Sam', 'Crewe-Sullam')
        self.p1_id = add_post_to_db('SuperCool', 'This is content', u_id)
        self.p2_id = add_post_to_db(
            'Major Post Here', 'misleading Titles are the worst', u_id)

    def tearDown(self):
        db.drop_all()
        db.create_all()

    def test_route_view_correct_post(self):
        with app.test_client() as client:
            res = client.get(f'/posts/{self.p1_id}')
            html = res.get_data(as_text=True)
            p1 = Post.query.get(self.p1_id)
            self.assertIn(p1.title, html)
            self.assertIn(p1.content, html)
            
    def test_route_returns_404_if_no_post(self):
        with app.test_client() as client:
            res = client.get(f'/posts/10')
            self.assertEqual(res.status_code, 404)


class CreatePostTests(TestCase):
    def setUp(self):
        self.u_id = add_user_to_db('Sam', 'Crewe-Sullam')
        self.p1_id = add_post_to_db('SuperCool', 'This is content', self.u_id)
        self.p2_id = add_post_to_db(
            'Major Post Here', 'misleading Titles are the worst', self.u_id)

    def tearDown(self):
        db.drop_all()
        db.create_all()

    def test_route_responds_with_corrent_page(self):
        with app.test_client() as client:
            res = client.get(f'/users/{self.u_id}/posts/new')
            self.assertEqual(res.status_code, 200)
            
            html = res.get_data(as_text=True)
            user = User.query.get(self.u_id)
            self.assertIn(f'{user.first_name} is making a post', html)

    def test_route_returns_404_if_no_user(self):
        with app.test_client() as client:
            res = client.get(f'/users/10/posts/new')
            self.assertEqual(res.status_code, 404)
    
    def test_post_route_redirects_to_user_details(self):
        with app.test_client() as client:
            res = client.post(f'/users/{self.u_id}/posts/new',
                              data={'title': 'New',
                                    'content': 'New post content!'})
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, f'http://localhost/users/{self.u_id}')

    def test_post_route_adds_post(self):
        post = Post.query.filter_by(
            title='New', content='New post content!').one_or_none()
        self.assertIsNone(post)

        with app.test_client() as client:
            res = client.post(f'/users/{self.u_id}/posts/new',
                              data={'title': 'New',
                                    'content': 'New post content!'},
                              follow_redirects=True)
            
            self.assertEqual(res.status_code, 200)
            
            post = Post.query.filter_by(
                title='New',content='New post content!').first()
            self.assertEqual(post.user_id, self.u_id)
        

def add_post_to_db(t, c, u_id):
    test_post = Post(title=t, content=c, user_id=u_id)
    db.session.add(test_post)
    db.session.commit()
    return test_post.id


def add_user_to_db(f, l, img=None):
    test_user = User(first_name=f, last_name=l, image_url=img)
    db.session.add(test_user)
    db.session.commit()
    return test_user.id


def get_html_from(path):
    with app.test_client() as client:
        res = client.get(path, follow_redirects=True)
        return res.get_data(as_text=True)
