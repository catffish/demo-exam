from flask_login import UserMixin
from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    offer = db.relationship('Offer', backref="author", lazy="dynamic")
    
    def __repr__(self):
        return 'user {}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Offer(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(250))
    category = db.Column(db.String(64), index=True)
    photo = db.Column(db.String(128))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    time = db.Column(db.DateTime, index=True)
    status = db.Column(db.String(10))
    reason = db.Column(db.String(120))

    def __repr__(self):
        return '<Offer {}>'.format(self.body)

class Category(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<Category {}>'.format(self.body)