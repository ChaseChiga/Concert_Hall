from app import app
from flask import session, render_template, request, redirect, flash
from datetime import datetime
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

@app.route('/shows/edit/<int:id>')
def get_edit_page(id):

    show =Show.get_by_id_with_creator(id)
    print(show.public)
    if 'update_form' in session:
        print(session['update_form'])
        show.name = session['update_form']['name']
        show.artists = session['update_form']['artists']
        show.location = session['update_form']['location']
        show.date = datetime.strptime(session['update_form']['date'], '%Y-%m-%d')
        show.rating = session['update_form']['rating']
        show.thoughts = session['update_form']['thoughts']
        show.public = int(session['update_form']['public'])
        session.pop('update_form')
        print(show.public)

    if 'user_id' not in session:
        return redirect('/logout')
    if show.creator.id != session['user_id']:
        flash("Can not edit someone elses show")
        return redirect('/logout')
    user_id = session['user_id']
    return render_template("edit.html", active_user = User.get_by_id(user_id), show =show)

@app.route('/shows/edit', methods= ['POST'])
def edit_sighting():
    show = Show.get_by_id_with_creator(int(request.form['id']))

    if show:
        if show.creator.id != session['user_id']:
            flash("Can not edit someone elses show")
            return redirect('/logout')
        
    if 'user_id' not in session:
        return redirect('/logout')
    
    if not Show.validate_new_show(request.form):
        session['update_form'] = request.form
        return redirect(f"/shows/edit/{show.id}")
    
    Show.edit(request.form)
    return redirect("/dashboard")

@app.route('/delete/<int:id>')
def delete_sighting(id):
    if 'user_id' not in session:
        return redirect('/logout') 
    if Show.get_by_id_with_creator(id).user_id != session['user_id']:
        flash("Can not delete someone elses sighting")
        return redirect('/logout')
    Show.delete(id)
    return redirect('/dashboard')

@app.route('/feed')
def get_feed():
    if 'user_id' not in session:
        return redirect('/logout')
    id = session['user_id']
    return render_template("feed.html", active_user = User.get_by_id(id), users_shows = Show.get_all_but_user(id))
