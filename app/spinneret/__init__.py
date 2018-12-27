from flask import Blueprint

spinneret = Blueprint('spinneret', __name__)

from . import routes