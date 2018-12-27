from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class SupplierForm(FlaskForm):
    display_as = StringField('Raison sociale', validators=[DataRequired()])
    first_name = StringField('Nom')
    last_name = StringField('Prénoms')
    phone = StringField('Téléphone')
    email = StringField('Email')
    submit = SubmitField('Enregistrer')
