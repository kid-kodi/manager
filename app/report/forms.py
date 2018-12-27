from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    from_date = StringField('De :', validators=[DataRequired()])
    to_date = StringField('A :', validators=[DataRequired()])
    submit = SubmitField('Executer')
