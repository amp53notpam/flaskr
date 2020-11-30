from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory
)
from werkzeug.exceptions import abort
from ..auth.auth import login_required
from ..models import db, User, Post
from .forms import CreateForm, UpdateForm, DeleteForm


blog_bp = Blueprint('blog_bp', __name__,
                    url_prefix='/blog',
                    static_folder='static',
                    template_folder='templates'
                    )


@blog_bp.route('/')
def index():
    posts = Post.query.join(User).\
        filter(Post.author_id == User.id).\
        with_entities(Post.id, Post.title, Post.body, Post.created, Post.author_id, User.username).\
        order_by(Post.created.desc()).\
        all()
    return render_template('index.jinja2', posts=posts)


@blog_bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = CreateForm()
    if form.validate_on_submit():
        title = request.form['title']
        body = request.form['body']

        new_post = Post(
            title=title,
            body=body,
            author_id=g.user.id
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('blog_bp.index'))

    return render_template('create.jinja2', form=form)


def get_post(id, check_author=True):
    post = Post.query.join(User).\
        filter(Post.author_id == User.id).\
        filter(Post.id == id).\
        with_entities(Post.id, Post.title, Post.body, Post.created, Post.author_id, User.username).\
        first_or_404(f"Post id {id} does not exist.")

    if check_author and post.author_id != g.user.id:
        abort(403)

    return post


@blog_bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)
    form_update = UpdateForm()
    form_update.body.data = post.body
    form_delete = DeleteForm()

    if form_update.validate_on_submit():
        post = Post.query.get(id)
        post.title = request.form['title']
        post.body = request.form['body']
        post.created = datetime.now()

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))

    return render_template('update.jinja2', post=post, form_update=form_update, form_delete=form_delete)


@blog_bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = Post.query.get(id)
    if post is not None:
        db.session.delete(post)
        db.session.commit()


@blog_bp.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(blog_bp.static_folder, filename)
