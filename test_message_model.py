"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_message_model.py


from app import app
import os
from unittest import TestCase

from models import db, User, Message, Follows

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


class MessageModelTestCase(TestCase):
    def setUp(self):
        Follows.query.delete()
        User.query.delete()
        Message.query.delete()
        db.create_all()

        self.app = app.test_client()
        self.app.testing = True

        # Create User objects with valid usernames, emails, and passwords
        user1 = User.signup('john', 'john@example.com', 'password', None)
        user2 = User.signup('susan', 'susan@example.com', 'password', None)

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        # Fetch the user objects from the database to ensure they have valid IDs
        self.user1 = User.query.get(user1.id)
        self.user2 = User.query.get(user2.id)

        # Create Message objects with valid text and associated users
        self.msg1 = Message(text="Hello", user_id=self.user1.id)
        self.msg2 = Message(text="Hi there!", user_id=self.user2.id)

        db.session.add(self.msg1)
        db.session.add(self.msg2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_message_model(self):
        user = User.signup('testuser', 'test@example.com', 'password', None)
        db.session.add(user)
        db.session.commit()

        message = Message(text="Test message", user_id=user.id)
        db.session.add(message)
        db.session.commit()

        self.assertEqual(message.text, "Test message")
