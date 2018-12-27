from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, \
    FieldList, HiddenField, Form as NoCsrfForm
from wtforms.fields import DateField, FormField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_babel import _, lazy_gettext as _l
from app.models import Purchase, PurchaseItem
from app import db


class SearchForm(FlaskForm):
    name = StringField(_l('Nom de la souche'))
    submit = SubmitField('Search')


# - - - Forms - - -
class PurchaseItemForm(NoCsrfForm):
    # this forms is never exposed so we can user the non CSRF version
    item_id = SelectField(_("Produit / Service"), coerce=int, choices=[])
    item_number = StringField(_('Nombre'), validators=[DataRequired()])
    item_price = StringField(_('Prix'), validators=[DataRequired()])
    item_amount = StringField(_('Montant'), validators=[DataRequired()])


class PurchaseForm(FlaskForm):
    supplier = SelectField(choices=[], coerce=int, label="Fournisseur")
    first_name = StringField(_l('Nom'), validators=[DataRequired()])
    last_name = StringField(_l('Prénoms'), validators=[DataRequired()])
    send_date = StringField(_l('Date de reception'))
    amount = StringField(_('Montant total'), validators=[DataRequired()])
    receive_date = StringField(_l('Date d\'envoi'))
    purchaseItems = FieldList(FormField(PurchaseItemForm, default=lambda:PurchaseItem()), min_entries=1)
    submit = SubmitField(_l('Enregistrer'))


class ValidateForm(FlaskForm):
    payment_type = SelectField('Type de paiement', coerce=int, choices=[(1, 'Chèque'), (2, 'Espèce')])
    number = StringField('Numéro')
    amount = StringField('Montant', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')
