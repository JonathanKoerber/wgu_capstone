
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    search = StringField('Search Posts', validators=[DataRequired()])
    submit = SubmitField('Search')

    # def validate_title(self, title):
    #     thread = Thread.query.filter_by(title=title.data).first()
    #     if thread:
    #         raise ValidationError('That thread title is already taken, Please choose a different one')
