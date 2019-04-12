from flask import session, redirect, url_for, render_template, request
from . import main
from .forms import LoginForm

names = []

@main.route('/', methods=['GET', 'POST'])
def index():
    """Login form to enter a room."""
    form = LoginForm()
    if request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
        return render_template('index.html', form=form)

    else:
        if form.name.data in names and form.name.data != session.get('name'):
            print('[!] Login error: user "{0}" already taken.'.format(form.name.data))
            return render_template('index.html', form=form, error='Username already in use.')
        if form.room.data == 'private' and form.name.data != 'admin':
            print('[!] Login error: permission denied for user "{0}" and room "{1}".'.format(form.name.data, form.room.data))
            return render_template('index.html', form=form, error='Room only accessable to user: admin')
        print('[*] User "{0}" joined "{1}".'.format(form.name.data, form.room.data))
        names.append(form.name.data)
        session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for('.chat'))

@main.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name')
    room = session.get('room')
    if name is None or room is None:
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room, safe=(room in ['feedback', 'safe']))
