# app/Item/views.py
from datetime import datetime
from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required

from . import bp
from .forms import SearchForm
from .. import db
from ..models import Order, Purchase, PurchaseItem, OrderItem, Item
from sqlalchemy.sql import func


# Item Views

@bp.route('/report', methods=['GET', 'POST'])
@login_required
def list():
    return render_template('report/list.html',
                           list=list, title="rapport")


@bp.route('/report/profit_and_lost', methods=['GET', 'POST'])
@login_required
def profit_and_lost():
    # orders = Order.query(func.sum(Order.amount).label("amount")).filter(Order.status == 1)
    orders = Order.query.filter(Order.status == 2)
    purchases = Purchase.query.filter(Purchase.status == 2)
    form = SearchForm()
    if form.validate_on_submit():
        # convert string to english format
        # convert english format to datetime
        # make the query
        _from_date = datetime.strptime(form.from_date.data, '%d-%m-%Y').strftime('%Y-%m-%d')
        _to_date = datetime.strptime(form.to_date.data, '%d-%m-%Y').strftime('%Y-%m-%d')

        orders = orders.filter(Order.created_at >= datetime.strptime(_from_date, '%Y-%m-%d'),
                               Order.created_at <= datetime.strptime(_to_date, '%Y-%m-%d')).all()

        purchases = purchases.filter(Purchase.created_at >= datetime.strptime(_from_date, '%Y-%m-%d'),
                                     Purchase.created_at <= datetime.strptime(_to_date, '%Y-%m-%d')).all()

    else:
        orders = orders.all()
        purchases = purchases.all()
    return render_template('report/profit_and_lost.html', orders=orders, purchases=purchases, title="rapport",
                           form=form)


@bp.route('/report/balance_sheet', methods=['GET', 'POST'])
@login_required
def balance_sheet():
    return render_template('report/balance_sheet.html',
                           list=list, title="rapport")


@bp.route('/report/expense_summary', methods=['GET', 'POST'])
@login_required
def expense_summary():
    # orders = Order.query(func.sum(Order.amount).label("amount")).filter(Order.status == 1)
    purchases = db.session.query(Item.name, PurchaseItem.item_price, db.func.sum(PurchaseItem.item_number).label("item_number"),
                                 db.func.sum(PurchaseItem.item_amount).label("item_amount"))\
                                .join(PurchaseItem, Item.purchase_items).group_by(Item.name)
    purchases = purchases.filter(Purchase.status == 2)
    form = SearchForm()
    if form.validate_on_submit():
        # convert string to english format
        # convert english format to datetime
        # make the query
        _from_date = datetime.strptime(form.from_date.data, '%d-%m-%Y').strftime('%Y-%m-%d')
        _to_date = datetime.strptime(form.to_date.data, '%d-%m-%Y').strftime('%Y-%m-%d')

        purchases = purchases.filter(PurchaseItem.created_at >= datetime.strptime(_from_date, '%Y-%m-%d'),
                                     PurchaseItem.created_at <= datetime.strptime(_to_date, '%Y-%m-%d')).all()

    else:
        purchases = purchases.all()
    return render_template('report/expense_summary.html',
                           list=list, title="rapport", purchases=purchases, form=form)


@bp.route('/report/sale_summary', methods=['GET', 'POST'])
@login_required
def sale_summary():
    # orders = Order.query(func.sum(Order.amount).label("amount")).filter(Order.status == 1)
    orders = db.session \
        .query(Item.name, OrderItem.item_price, db.func.sum(OrderItem.item_number).label("item_number"),
               db.func.sum(OrderItem.item_amount).label("item_amount")) \
        .join(OrderItem, Item.order_items).group_by(Item.name)
    orders = orders.filter(Purchase.status == 2)
    form = SearchForm()
    if form.validate_on_submit():
        # convert string to english format
        # convert english format to datetime
        # make the query
        _from_date = datetime.strptime(form.from_date.data, '%d-%m-%Y').strftime('%Y-%m-%d')
        _to_date = datetime.strptime(form.to_date.data, '%d-%m-%Y').strftime('%Y-%m-%d')

        orders = orders.filter(OrderItem.created_at >= datetime.strptime(_from_date, '%Y-%m-%d'),
                               OrderItem.created_at <= datetime.strptime(_to_date, '%Y-%m-%d')).all()

    else:
        orders = orders.all()
    return render_template('report/sale_summary.html',
                           list=list, title="rapport", orders=orders, form=form)
