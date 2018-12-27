from flask import Blueprint

bp = Blueprint('report', __name__, template_folder="templates")

from . import routes, forms