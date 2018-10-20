from flask import Flask, redirect, render_template, flash, url_for, request
from werkzeug.urls import url_parse
from forms import Login
from flask_login import login_user, LoginManager, current_user, logout_user, login_required
from scripts.models import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 's3cr3tk3y'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
login = LoginManager(app)
login.init_app(app)
# daba ay page dhklti liha fiha unauthorised access tay redirectik l hna '/login' instead of showing you 401 error
login.login_view = '/login'

@login.user_loader
def load_user(id):
     return User.query.get(id)

db = SQLAlchemy(app)

@app.route('/')
@app.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('register.html')



@app.route('/login', methods=['GET','POST'])
def get_login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Login()
    next_url = request.args.get('next')
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_pass(form.password.data):
            flash('Invalid username or password')
            return redirect('login')
        else:
        # DONT FORGET THAT ABDELALI
         login_user(user, remember=form.remember_me.data)
        # DONT FORGET THIS LINE ABOVE

         if not next_url or url_parse(next_url).netloc != '':
             next_url = url_for('index')
         flash('Logged Successfully ')
         return redirect(next_url)
    else:
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/signout', methods=['GET'])
def signout():
     logout_user()
     flash('Good Bye !')
     return redirect(url_for('get_login'))










if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

