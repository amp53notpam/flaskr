#! venv/bin/python

from flaskr import create_app
from flask.cli import FlaskGroup
from flaskr import db

cli = FlaskGroup(create_app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    cli()
