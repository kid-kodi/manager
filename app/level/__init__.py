from flask import Blueprint

level = Blueprint('level', __name__)

from . import routes