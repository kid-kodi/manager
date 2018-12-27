from flask import Blueprint

bp = Blueprint('purchase', __name__, template_folder="templates")

from . import routes, forms