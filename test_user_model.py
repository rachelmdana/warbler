"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


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


class UserModelTestCase(TestCase):
    def setUp(self):
        # Create a test client and clear the database
        self.client = app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        # Remove the session and drop the database
        db.session.remove()
        db.drop_all()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"  # Provide a valid password
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_repr_method(self):
        user = User(username="testuser", email="test@example.com",
                    password="HASHED_PASSWORD")  # Provide a valid password
        db.session.add(user)
        db.session.commit()
        self.assertEqual(
            repr(user), f"<User #{user.id}: {user.username}, {user.email}>")

    def test_is_following(self):
        user1 = User(username="user1", email="user1@example.com",
                     password="HASHED_PASSWORD")  # Provide a valid password
        user2 = User(username="user2", email="user2@example.com",
                     password="HASHED_PASSWORD")  # Provide a valid password
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        user1.following.append(user2)
        db.session.commit()
        self.assertTrue(user1.is_following(user2))
        self.assertFalse(user2.is_following(user1))
