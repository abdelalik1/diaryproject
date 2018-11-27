from run import db, login
from datetime import datetime
from hashlib import md5
from flask_login import UserMixin




class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(30), index=True)
    username = db.Column(db.String(9), index=True)
    email = db.Column(db.String(11), unique=True)
    password = db.Column(db.String(15))
    

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return "<User {} >".format(self.username)

    def md5hash(self, usr):
        self.password = md5(usr.encode('utf-8')).hexdigest()
    def avatar(self, size):
        encemail = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'http://gravatar.com/avatar/{}/?d=identicon&s={}'.format(encemail, size)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(20))
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "<Post {} >".format(self.body)




