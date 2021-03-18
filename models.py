from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True, unique=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.Text, nullable=False)

    allstar = db.relationship('Allstar', backref='user')

    @classmethod
    def register(cls, username, email, pwd):
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, email=email, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, pwd):
        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False

class Allstar(db.Model):
    __tablename__ = 'allstars'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    img = db.Column(db.Text, nullable=False)
    quote = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, db.ForeignKey('users.username'))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'img': self.img,
            'quote': self.quote,
            'username': self.username
        }

    
    
    
