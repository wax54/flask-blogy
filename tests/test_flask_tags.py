from unittest import TestCase
from tests import get_html_from, app
from models import db, connect_db, DEFAULT_IMAGE_URL
from models.Tag import Tag

app.config['TESTING'] = True
app.config['SQLALCHEMY_ECHO'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'

connect_db(app)
db.drop_all()
db.create_all()


class TagListRouteTests(TestCase):
    def setUp(self):
        add_tag_to_db('Sam')
        add_tag_to_db('Fun')
        add_tag_to_db('Exciting')

    def tearDown(self):
        db.drop_all()
        db.create_all()

    def test_returns_tags(self):
        html = get_html_from('/tags')
        self.assertIn('Sam', html)
        self.assertIn('Fun', html)
        self.assertIn('Exciting', html)


class NewTagRouteTests(TestCase):
    def tearDown(self):
        db.drop_all()
        db.create_all()

    def test_get_route_returns_correct_page(self):
        self.assertIn('<h1>New Tag!</h1>', get_html_from('/tags/new'))

    def test_post_route_redirects_to_tag_list(self):
        with app.test_client() as client:
            res = client.post('/tags/new',
                              data={'name': 'new_tag'})
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, 'http://localhost/tags')

    def test_post_route_adds_tag(self):
        with app.test_client() as client:
            tags = Tag.query.filter_by(
                name='Unique Tag').all()
            #user doesn't exist yet
            self.assertEqual(tags, [])

            res = client.post('/tags/new',
                              data={'name': 'Unique Tag'},
                              follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('Unique Tag', res.get_data(as_text=True))
            tag = Tag.query.filter_by(
                name='Unique Tag').one_or_none()
            self.assertEqual(tag.name, 'Unique Tag')

    def test_post_route_rejects_no_name(self):
        with app.test_client() as client:
            res = client.post('/tags/new',
                              data={'name': ''},
                              follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            tag = Tag.query.filter_by(name="").one_or_none()
            #tag was never made
            self.assertIsNone(tag)

    def test_post_route_rejects_repeats(self):
        with app.test_client() as client:
            res = client.post('/tags/new',
                              data={'name': 'Sam'},
                              follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            res = client.post('/tags/new',
                              data={'name': 'Sam'},
                              follow_redirects=True)
            self.assertEqual(res.status_code, 200)

            html = res.get_data(as_text=True)
            self.assertIn('I think We already got that Tag!', html)


class EditTagsTests(TestCase):
    def setUp(self):
        self.sam_id = add_tag_to_db('Sam')
        self.fun_id = add_tag_to_db('fun')
        self.exciting_id = add_tag_to_db('exciting')

    def tearDown(self):
        db.drop_all()
        db.create_all()

    def test_get_route_returns_correct_page(self):
        html = get_html_from(f'/tags/{self.sam_id}/edit')
        self.assertIn('<h1>Edit Tag "Sam"!</h1>', html)

    def test_post_route_redirects_to_all_tags_page(self):
        with app.test_client() as client:
            res = client.post(f'/tags/{self.sam_id}/edit',
                              data={'name': 'John'})
            self.assertEqual(res.status_code, 302)
            self.assertEqual(
                res.location, 'http://localhost/tags')
            res = client.get(res.location)
            html = res.get_data(as_text=True)
            self.assertIn('John', html)

    def test_post_route_edits_tag_info(self):
        with app.test_client() as client:
            fun_tag = Tag.query.get(self.fun_id)
            self.assertEqual(fun_tag.name, 'fun')
            res = client.post(f'/tags/{self.fun_id}/edit',
                              data={'name': 'Benny'},
                              follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            fun_tag = Tag.query.get(self.fun_id)
            self.assertEqual(fun_tag.name, 'Benny')

    def test_post_route_rejects_no_name(self):
        with app.test_client() as client:

            res = client.post(f'/tags/{self.sam_id}/edit',
                              data={'name': ''},
                              follow_redirects=True)
            self.assertEqual(res.status_code, 200)

            sam = Tag.query.get(self.sam_id)
            self.assertNotEqual(sam.name, '')
            # No change was made
            self.assertEqual(sam.name, 'Sam')


class DeleteTagTests(TestCase):
    def setUp(self):
        self.sam_id = add_tag_to_db('Sam')
        self.fun_id = add_tag_to_db('fun')
        self.exciting_id = add_tag_to_db('exciting')

    def tearDown(self):
        db.drop_all()
        db.create_all()

    def test_route_deletes_user(self):
        with app.test_client() as client:
            res = client.get(
                f'/tags/{self.sam_id}/delete', follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            sam = Tag.query.get(self.sam_id)
            self.assertIsNone(sam)

    def test_post_route_redirects_to_tag_list(self):
        with app.test_client() as client:
            res = client.get(f'/tags/{self.fun_id}/delete')

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, 'http://localhost/tags')
            res = client.get(res.location)
            html = res.get_data(as_text=True)
            self.assertNotIn('fun', html)


def add_tag_to_db(name):
    test_tag = Tag(name=name)
    db.session.add(test_tag)
    db.session.commit()
    return test_tag.id
