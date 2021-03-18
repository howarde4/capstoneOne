from unittest import TestCase
from flask import session
from app import app
from models import db, User, Allstar

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///drag_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

db.drop_all()
db.create_all()

ALLSTAR_DATA = {
    "name": "Trixie",
    "image": "trixie.jpg",
    "quote": 'im trixie',
    "username": "iamatest"
}

class AllStarTest(TestCase):
    @classmethod
    def setUpClass(cls):
        user = User(username="iamatest", email="testing@t.com", password="testpw")
        db.session.add(user)
        db.session.commit()
        Allstar.query.delete()
        allstar = Allstar(name='Milk', img='milk.jpg', quote='milk does the body good', username='iamatest')
        db.session.add(allstar)
        db.session.commit()

        cls.allstar = allstar.username

    @classmethod
    def tearDownClass(cls): 
        db.session.rollback()

    def test_allstar_form(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['username'] = 'iamatest'

            res = client.post('/users/iamatest/allstars', json=ALLSTAR_DATA)

            self.assertEqual(res.status_code, 201)