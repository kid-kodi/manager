# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, FileField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app import images

from ..models import User


class CompanyForm(FlaskForm):
    image = FileField('Logo', validators=[FileAllowed(images, 'Images seulement')])
    registration_number = HiddenField(validators=[DataRequired()])
    company_name = StringField('Nom de la société', validators=[DataRequired()])
    email = StringField('Adresse email', validators=[DataRequired(), Email()])
    phone = StringField('Téléphone', validators=[DataRequired()])
    web_site = StringField('Site web')
    address = StringField('Adresse')
    submit = SubmitField('Enregistrer')


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('confirm_password')
    ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')
