from run import db, login
from datetime import datetime
from werkzeug import security
from flask_login import UserMixin




class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(9), unique=True, index=True)
    email = db.Column(db.String(11), index=True, unique=True)
    password = db.Column(db.String(15))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return "<User {} >".format(self.username)

    def set_password_hash(self, passwordd):
        self.password = security.generate_password_hash(passwordd)


    def check_pass(self, password):
        return security.check_password_hash(self.password, password)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(20))
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "<Post {} >".format(self.body)
