from unittest import TestCase
from flask import session
from app import app
from models import db, User, Allstar

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///drag_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

db.drop_all()
db.create_all()

class DragTestCase(TestCase):

    @classmethod
    def setUp(cls):
        User.query.delete()
        user = User(username="iamatest", email="testing@t.com", password="testpw")
        db.session.add(user)
        db.session.commit()

        cls.username = user.username

    @classmethod
    def tearDown(cls): 
        db.session.rollback()

    def test_redirect(self):
        with app.test_client() as client:
            res = client.get('/')

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, 'http://localhost/register')

    def test_register(self):
        with app.test_client() as client:
            res = client.get('/register')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h2>Register Below!</h2>', html)

    def test_login(self):
        with app.test_client() as client:
            res = client.get('/login')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="display-4" id="login">Login:</h1>', html)

    def test_register_form(self):
        with app.test_client() as client:
            res = client.post('/register', data={'username': 'testuser', 'email': 'test@t.com', 'password': 'testing'})
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h2>Register Below!</h2>', html)

    def test_login_form(self):
        with app.test_client() as client:
            res = client.post('/login', data={'username': 'testuser', 'password': 'testing'})
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="display-4" id="login">Login:</h1>', html)

    def test_session(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['username'] = 'iamatest'

            res = client.get('/login')
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, 'http://localhost/users/iamatest')

    def test_allstar(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['username'] = 'iamatest'

            res = client.get('/users/iamatest/allstars')
            self.assertEqual(res.status_code, 200)
