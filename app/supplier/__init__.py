from flask import Blueprint

bp = Blueprint('supplier', __name__)

from . import routes, forms
