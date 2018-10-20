from models import User, Post
from run import db


#a = User(username='manal', email='manal@gmail.com', password='manal2312@')
#db.session.add(a)
#db.session.commit()

b = User(username='admin', email='abdelali@khalfi.me')
b.set_password_hash('abdelali123')
db.session.add(b)
db.session.commit()
