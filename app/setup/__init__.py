from flask import Blueprint

setup = Blueprint('setup', __name__, template_folder="templates")

from . import routes