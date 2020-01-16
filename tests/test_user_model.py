import unittest
import time
from app import db  
from app.models import User, Permission, AnonymousUser, Role

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_valid_confirmation_token(self):
        u = User()
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))
        self.assertTrue(u.confirmed)

    def test_invalid_confirmation_token(self):
        u1 = User()
        u2 = User()
        db.session.add_all([u1, u2])
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))
        self.assertFalse(u2.confirmed)

    def test_expired_confirmation_token(self):
        u = User()
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(expiration=1)
        time.sleep(2)
        self.assertFalse(u.confirm(token))

    def test_valid_reset_token(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertTrue(User.reset_password(token, 'dog'))
        self.assertTrue(u.verify_password('dog'))

    def test_invalid_reset_token(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertFalse(User.reset_password(token + 'a', 'dog'))
        self.assertTrue(u.verify_password('cat'))

    def test_valid_email_change_token(self):
        u = User(email='foo@example.com', password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_email_change_token('bar@example.com')
        self.assertTrue(u.change_email(token))
        self.assertEqual(u.email, 'bar@example.com')

    def test_email_change_token(self):
        u = User(email='foo@example.com')
        db.session.add(u)
        db.session.commit()
        token = u.generate_email_change_token('bar@example.com')
        self.assertFalse(u.change_email(token + 'a'))
        self.assertNotEqual(u.email, 'bar@example.com')
        self.assertEqual(u.email, 'foo@example.com')

    def test_duplicate_email_change_token(self):
        u1 = User(email='john@example.com')
        u2 = User(email='peter@example.com')
        db.session.add_all([u1, u2])
        db.session.commit()
        token = u1.generate_email_change_token('peter@example.com')
        self.assertFalse(u1.change_email(token))
        self.assertEqual(u1.email, 'john@example.com')

    def test_user_role(self):
        u = User(email='john@example.com', password='cat')
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))
        self.assertFalse(u.can(Permission.COMMENT))
        self.assertFalse(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))
