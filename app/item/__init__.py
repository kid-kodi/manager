from flask import Blueprint

bp = Blueprint('item', __name__, template_folder="templates")

from . import routes, forms