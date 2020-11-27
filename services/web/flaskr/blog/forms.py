from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class CreateForm(FlaskForm):
    title = StringField("Title", [DataRequired()])
    body = TextAreaField("Body", [DataRequired()])
    submit = SubmitField('Save')


class UpdateForm(FlaskForm):
    title = StringField("Title", [DataRequired()])
    body = TextAreaField("Body")
    submit = SubmitField('Save')


class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')
