from flask import Blueprint

unit = Blueprint('unit', __name__)

from . import routes