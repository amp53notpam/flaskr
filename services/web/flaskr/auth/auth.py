import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from ..models import db, User, Post
from .forms import RegisterForm, LogInForm

auth_bp = Blueprint('auth_bp', __name__,
                    url_prefix='/auth',
                    static_folder='static',
                    template_folder='templates'
                    )


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(** kwargs):
        if g.user is None:
            return redirect(url_for('auth_bp.login'))

        return view(**kwargs)

    return wrapped_view


@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter(User.id == user_id).first()


@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        error = None

        if User.query.filter(User.username == username).first() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            new_user = User(
                username=username,
                password=generate_password_hash(password)
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth_bp.login'))

        flash(error)

    return render_template('register.jinja2', form=form)


@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LogInForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        error = None

        user = User.query.filter(User.username == username).first()

        if user is None:
            error = True
        elif not check_password_hash(user.password, password):
            error = True

        if error:
            error = 'Wrong username or password.'
        else:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('blog_bp.index'))

        flash(error)

    return render_template('login.jinja2', form=form)


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blog_bp.index'))
