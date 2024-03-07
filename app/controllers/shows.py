from app import app
from flask import session, render_template, request, redirect, flash
from app.models.user import User
from app.models.show import Show


@app.route('/shows/new')
def get_add_page():
    if 'user_id' not in session:
        return redirect('/logout')
    id = session['user_id']
    return render_template("add.html", active_user = User.get_by_id(id))

@app.route('/shows/new', methods= ['POST'])
def add_show():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Show.validate_new_show(request.form):
        return redirect('/shows/new')
    Show.create(request.form)
    return redirect("/dashboard")

@app.route('/shows/<int:id>')
def get_view_page(id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_id = session['user_id']
    return render_template("view.html", active_user = User.get_by_id(user_id), show = Show.get_by_id_with_creator(id),)
