from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    searchbox = StringField('Search Here?', validators=[DataRequired()])
    submit = SubmitField('Search')