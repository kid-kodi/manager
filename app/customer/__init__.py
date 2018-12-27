from flask import Blueprint

bp = Blueprint('customer', __name__)

from . import routes, forms