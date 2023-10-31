"""User view tests."""

# run these tests like:
#
#    python -m unittest test_user_views.py

from app import app
import os
from unittest import TestCase

from models import db, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class ViewUsersTestCase(TestCase):
    def setUp(self):
        self.app = app.test_client()
        # We want to start with a blank slate on every test
        db.drop_all()
        db.create_all()

        # Create User objects with valid usernames, emails, and passwords
        self.john = User.signup('john', 'john@example.com', 'password', None)
        self.mary = User.signup('mary', 'mary@example.com', 'password', None)
        self.dave = User.signup('dave', 'dave@example.com', 'password', None)
        self.emily = User.signup(
            'emily', 'emily@example.com', 'password', None)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, user):
        return self.app.post('/login', data=dict(
            username=user.username, password='password'), follow_redirects=True)

    def logout(self):
        return self.app.get("/logout", follow_redirects=True)

    def test_empty_page(self):
        User.query.delete()
        db.session.commit()

        response = self.app.get('/users')
        assert b'Sorry, no users found' in response.data

    def test_view_user_profile(self):
        response = self.app.get('/users/1')
        self.assertEqual(response.status_code, 200)
