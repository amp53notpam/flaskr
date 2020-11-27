from flask import current_app as app
from flask import make_response, redirect, render_template, request, url_for


@app.route('/')
def start():
    return redirect(url_for('blog_bp.index'))


@app.route('/hello')
def hello():
    return "Hello, world!"
