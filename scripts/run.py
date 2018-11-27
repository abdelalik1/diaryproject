from flask import Flask, redirect, render_template, flash, url_for, request
from werkzeug.urls import url_parse
from forms import *
from flask_login import login_user, LoginManager, current_user, logout_user, login_required
from scripts.models import *
from flask_sqlalchemy import SQLAlchemy
from hashlib import md5

app = Flask(__name__)
app.secret_key = 's3cr3tk3y'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DATABASE.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
    namee = current_user.fullname
    return render_template('index.html', namee=namee)



@app.route('/login', methods=['GET','POST'])
def get_login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Login()
    next_url = request.args.get('next')
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        email = User.query.filter_by(email=form.username.data)
        check_pass = md5(form.password.data.encode('utf-8')).hexdigest()
        if user  is None or check_pass != user.password:


            flash('Invalid password')
            return redirect('login')
        else:

         login_user(user, remember=form.remember_me.data)


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        usr = User(fullname=form.fullname.data, email=form.email.data, username=form.username.data)
        usr.md5hash(form.password.data)
        db.session.add(usr)
        db.session.commit()
        flash('Successfull registration !')
        return redirect(url_for('get_login'))

    return render_template('register.html', form=form, title='Register Page')

@app.route('/user/<id>')
@login_required
def profil(id):
    ali = User.query.filter_by(id=id).first_or_404()
    return render_template('user.html', title='Profile Page', ali=ali)

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditForm()
    if form.validate_on_submit():
        current_user.fullname = form.fullname.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Successfully updated')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.fullname.data = current_user.fullname
        form.email.data = current_user.email
    return render_template('edit.html', title='Edit Profile Page', form=form)










if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)

