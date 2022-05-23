from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField, BooleanField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    searchbox = StringField('', validators=[DataRequired()])
    result = SelectField('Results', choices=[(5, 5), (10, 10),(20, 20),(30, 30)])
    type_res = SelectField('Type', choices=[("ALL", "ALL"), ("PDF", "PDF"),("Web", "Web")])
    submit = SubmitField('Search')