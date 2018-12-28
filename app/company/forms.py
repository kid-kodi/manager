# app/departement/forms.py

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email
from app import images


class SearchForm(FlaskForm):
    first_name = StringField('first name')
    last_name = StringField('last name')
    unit_id = SelectField('Search unit', choices=[], coerce=int)
    submit = SubmitField('Search')


class CompanyForm(FlaskForm):
    image = FileField('Logo', validators=[FileAllowed(images, 'Images seulement')])
    registration_number = HiddenField(validators=[DataRequired()])
    company_name = StringField('Nom de la société', validators=[DataRequired()])
    email = StringField('Adresse email', validators=[DataRequired(), Email()])
    phone = StringField('Téléphone', validators=[DataRequired()])
    web_site = StringField('Site web', validators=[DataRequired()])
    address = StringField('Adresse', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')
