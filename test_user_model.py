"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///sharebnb_test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", "userFirst1","userLast1" )
        u2 = User.signup("u2", "u2@email.com", "password", "userFirst2","userLast2" )

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        u1 = User.query.get(self.u1_id)

    # #################### Signup Tests

    def test_valid_signup(self):
        u1 = User.query.get(self.u1_id)

        self.assertEqual(u1.username, "u1")
        self.assertEqual(u1.email, "u1@email.com")
        self.assertNotEqual(u1.password, "password")
        # Bcrypt strings should start with $2b$
        self.assertTrue(u1.password.startswith("$2b$"))

    # #################### Authentication Tests

    def test_valid_authentication(self):
        u1 = User.query.get(self.u1_id)

        u = User.authenticate("u1", "password")
        self.assertEqual(u, u1)

    def test_invalid_username(self):
        self.assertFalse(User.authenticate("bad-username", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate("u1", "bad-password"))
