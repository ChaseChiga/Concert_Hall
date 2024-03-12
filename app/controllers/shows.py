import os
import uuid
from app import app
from flask import session, render_template, request, redirect, flash, url_for, send_file
from werkzeug.utils import secure_filename
from datetime import datetime
from app.models.user import User
from app.models.show import Show

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/shows/new')
def get_add_page():
    show = {}
    
    if 'user_id' not in session:
        return redirect('/logout')
    if 'update_form' in session:
        show = session['update_form']
        if show['date'] != '':
            show['date'] = datetime.strptime(show['date'], '%Y-%m-%d')
        session.pop('update_form')
    id = session['user_id']
    return render_template("add.html", active_user = User.get_by_id(id), show = show)

@app.route('/shows/new', methods= ['POST'])
def add_show():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Show.validate_new_show(request.form):
        session['update_form'] = request.form
        return redirect('/shows/new')
        # check if the post request has the file part
    filename = None
    print(request.files)
    if 'file_name' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file_name']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
    if file and allowed_file(file.filename):
        filename = uuid.uuid4().hex
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    Show.create({
        **request.form,
        'file_name': filename
    })
    if 'update_form' in session:
        session.pop('update_form')
    return redirect("/dashboard")

@app.route('/shows/<int:id>')
def get_view_page(id):

    show = Show.get_by_id_with_creator(id) 
    if 'user_id' not in session:
        return redirect('/logout')
    if show.creator.id != session['user_id'] and show.public == 0:
        flash("this post is private or does not exist")
        return redirect('/feed')
    data = {
        "show_id": id, 
        "user_id": session['user_id']
    }
    user_id = session['user_id']
    liked = Show.get_like_from_user(data)
    return render_template("view.html", active_user = User.get_by_id(user_id), show = show, liked = liked)

@app.route('/shows/edit/<int:id>')
def get_edit_page(id):

    show =Show.get_by_id_with_creator(id)
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

    if 'user_id' not in session:
        return redirect('/logout')
    if show.creator.id != session['user_id']:
        flash("Can not edit someone elses show")
        return redirect('/logout')
    user_id = session['user_id']
    return render_template("edit.html", active_user = User.get_by_id(user_id), show =show)

@app.route('/shows/edit', methods= ['POST'])
def edit_showing():
    show = Show.get_by_id_with_creator(int(request.form['id']))
    if "file_name" not in session:
        session['file_name'] = show.file_name
        print(f"!!!!!! {show.file_name}")

    if show:
        if show.creator.id != session['user_id']:
            flash("Can not edit someone elses show")
            return redirect('/logout')
        
    if 'user_id' not in session:
        return redirect('/logout')
    
    if not Show.validate_new_show(request.form):
        session['update_form'] = request.form
        return redirect(f"/shows/edit/{show.id}")
    
    filename = None
    if 'file_name' not in request.files:
        flash('No file part')
        session['update_form'] = request.form
        return redirect(f'/shows/edit/{show.id}')
    file = request.files['file_name']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
    if file.filename == '':
            if 'remove_image' not in request.form:
                show.edit({
                    **request.form,
                    'file_name': session['file_name']
                })
            else:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], session['file_name']))
                show.edit({
                    **request.form,
                    'file_name': None
                })
            session.pop('file_name')
            return redirect('/dashboard')
    if file and allowed_file(file.filename):
        filename = uuid.uuid4().hex
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if session['file_name'] != None:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], session['file_name']))
    Show.edit({
        **request.form,
        'file_name': filename
    })
    session.pop('file_name')
    return redirect("/dashboard")

@app.route('/delete/<int:id>')
def delete_sighting(id):
    if 'user_id' not in session:
        return redirect('/logout') 
    show = Show.get_by_id_with_creator(id)
    if show.user_id != session['user_id']:
        flash("Can not delete someone elses sighting")
        return redirect('/logout')
    if show.user_id == session['user_id']:
        if show.file_name != None:
            if "file_name" not in session:
                session['file_name'] = show.file_name
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], session['file_name']))
            session.pop('file_name')
    Show.delete(id)
    return redirect('/dashboard')

@app.route('/feed')
def get_feed():
    if 'user_id' not in session:
        return redirect('/logout')
    id = session['user_id']
    likes = Show.count_likes()
    print(likes)
    return render_template("feed.html", active_user = User.get_by_id(id), users_shows = Show.get_all_but_user(id), likes = likes)

@app.route('/shows/add/like', methods= ['POST'])
def add_like():
    if 'user_id' not in session:
        return redirect('/logout')
    Show.add_like(request.form)
    return redirect(f'/shows/{request.form['show_id']}')

@app.route('/shows/remove/like', methods= ['POST'])
def remove_like():
    print(request.form)
    if 'user_id' not in session:
        return redirect('/logout')
    Show.delete_likes(request.form)
    return redirect(f'/shows/{request.form['show_id']}')

@app.route('/shows/image/<int:id>')
def get_image(id):
    show = Show.get_by_id_with_creator(id)
    print(f'this is the result: {show.file_name}')
    return send_file(os.path.abspath(app.config['UPLOAD_FOLDER'] + '/' + show.file_name), mimetype='image/png')
