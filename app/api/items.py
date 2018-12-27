from flask import jsonify, request, url_for
from app import db
from app.models import Item
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request


@bp.route('/item/')
def get_items():
    items = Item.query.all()
    return jsonify([item.to_json() for item in items])


@bp.route('/item/<int:id>')
def get_item(id):
    item = Item.query.get_or_404(id)
    return jsonify(item.to_json())


