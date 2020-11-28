import os
from threading import Lock

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)

    if test_config is None:
        app.config.from_object('flaskr.config.Config')
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)

    with app.app_context():
        # Include our Routes
        from . import routes

        # Register Blueprints
        from .auth import auth
        app.register_blueprint(auth.auth_bp)

        from .blog import blog
        app.register_blueprint(blog.blog_bp)

        return app
