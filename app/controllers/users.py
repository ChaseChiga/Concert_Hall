from app import app
from flask_bcrypt import Bcrypt
from flask import session, render_template, request, redirect, flash
from app.models.user import User
from app.models.show import Show

bcrypt = Bcrypt(app)
@app.route('/')
def home():

    return render_template("index.html")

@app.route('/register')
def register():

    return render_template("register.html")

@app.route('/register', methods = ['POST'])
def register_user():
    if not User.validate_new_user(request.form):
        return redirect('/register')
    hashed_password = bcrypt.generate_password_hash(request.form['password'])
    User.register({**request.form,
                "password": hashed_password})
    new_user = User.get_by_email(request.form['email'])
    session['user_id'] = new_user.id
    return redirect('/dashboard')

@app.route('/login')
def login():

    return render_template("login.html")

@app.route('/login', methods = ['POST'])
def login_user():
    user_exist = User.get_by_email(request.form['email'])
    if not user_exist:
        flash('invalid email or password')
        return redirect("/login")
    if not bcrypt.check_password_hash(user_exist.password, request.form['password']):
        flash('invalid email or password')
        return redirect("/login")
    session['user_id'] = user_exist.id
    print(session['user_id'])
    return redirect("/dashboard")

@app.route('/dashboard')
def get_dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    id = session['user_id']
    likes = Show.count_likes()
    return render_template("dashboard.html", active_user = User.get_by_id(id), user_shows = Show.get_by_creator(id), likes = likes)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')