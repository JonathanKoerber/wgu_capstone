from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from orange_it.models import Thread


class ThreadForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Create Thread')

    def validate_title(self, title):
        thread = Thread.query.filter_by(title=title.data).first()
        if thread:
            raise ValidationError('That thread title is already taken, Please choose a different one')

class Update_Thread(FlaskForm):

    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Update Tread')


