from unittest import TestCase
from app import app

app.config['TESTING'] = True


class UserListRouteTests(TestCase):
    def test_returns_user():
        client = app.test_client()
        print(client.get('/users'))
