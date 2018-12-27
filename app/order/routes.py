# app/Order/views.py
from datetime import datetime
from flask import abort, flash, redirect, request, render_template, url_for
from flask_login import current_user, login_required

from . import bp
from .forms import OrderForm, SearchForm, ValidateForm
from .. import db
from ..models import Order, Customer, OrderItem, Item, Invoice


# Order Views

@bp.route('/order', methods=['GET', 'POST'])
@login_required
def index():
    pagination = []
    search_form = SearchForm()
    page = request.args.get('page', 1, type=int)
    if search_form.validate_on_submit():
        name = search_form.name.data
        if name != '':
            pagination = Order.query.filter_by(name=name) \
                .order_by(Order.created_at.desc()).paginate(
                page, per_page=50,
                error_out=False)
        else:
            pagination = Order.query \
                .order_by(Order.created_at.desc()).paginate(
                page, per_page=50,
                error_out=False)
    else:
        pagination = Order.query \
            .order_by(Order.created_at.desc()).paginate(
            page, per_page=50,
            error_out=False)
    list = pagination.items
    return render_template('order/list.html',
                           list=list, pagination=pagination,
                           title="orders", search_form=search_form)


@bp.route('/order/add', methods=['GET', 'POST'])
@login_required
def add():
    add = True
    form = OrderForm()
    form.customer.choices = [(c.id, c.display_as) for c in Customer.query.all()]
    for x in form.orderItems.entries:
        x.item_id.choices = [(c.id, c.name) for c in Item.query.all()]

    if form.validate_on_submit():
        order = Order(customer_id=form.customer.data,
                      serial=item_serial(),
                      first_name=form.first_name.data,
                      last_name=form.last_name.data,
                      send_date=form.send_date.data,
                      receive_date=form.receive_date.data,
                      amount=form.amount.data,
                      status=0,
                      created_by=current_user.id,
                      created_at=datetime.utcnow())
        db.session.add(order)
        db.session.commit()

        order_items = form.orderItems.entries
        for order_item in order_items:
            print(order_item.item_id.data)
            print(order_item.item_number.data)
            print(order_item.item_price.data)
            print(order_item.item_amount.data)
            order_item = OrderItem(order_id=order.id,
                                   item_id=order_item.item_id.data,
                                   item_number=order_item.item_number.data,
                                   item_price=order_item.item_price.data,
                                   item_amount=order_item.item_amount.data,
                                   created_by=current_user.id,
                                   created_at=datetime.utcnow())
            db.session.add(order_item)
            db.session.commit()

        flash('You have successfully saved the order.')

        # redirect to the bps page
        return redirect(url_for('order.index'))

    return render_template('order/form.html', action="Add",
                           add=add, form=form,
                           title="Add order")


@bp.route('/order/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    add = False
    order = Order.query.get_or_404(id)
    form = OrderForm(obj=order)
    form.customer.choices = [(c.id, c.display_as) for c in Customer.query.all()]
    for x in form.orderItems.entries:
        x.item_id.choices = [(c.id, c.name) for c in Item.query.all()]

    if form.validate_on_submit():
        order.customer_id = form.customer.data
        order.first_name = form.first_name.data
        order.last_name = form.last_name.data
        order.send_date = form.send_date.data
        order.receive_date = form.receive_date.data
        order.amount = form.amount.data
        order.order_items = []
        db.session.commit()
        order_items = form.orderItems.entries
        for order_item in order_items:
            _item = OrderItem(order_id=order.id,
                              item_id=order_item.item_id.data,
                              item_number=order_item.item_number.data,
                              item_price=order_item.item_price.data,
                              item_amount=order_item.item_amount.data)
            db.session.add(_item)
            db.session.commit()
        flash('You have successfully edited the order.')

        # redirect to the bps page
        return redirect(url_for('order.index'))

    form.customer.data = order.customer_id
    form.first_name.data = order.first_name
    form.last_name.data = order.last_name
    form.send_date.data = order.send_date
    form.receive_date.data = order.receive_date

    for order_item in order.order_items:
        form.orderItems.append_entry(order_item)

    for x in form.orderItems.entries:
        x.item_id.choices = [(c.id, c.name) for c in Item.query.all()]
    return render_template('order/form.html', action="Edit",
                           add=add, form=form,
                           order=order, title="Edit order")


@bp.route('/order/<int:id>', methods=['GET', 'POST'])
@login_required
def detail(id):
    form = ValidateForm()
    order = Order.query.get_or_404(id)
    if form.validate_on_submit():
        invoice = Invoice()
        invoice.serial = invoice_serial()
        invoice.order_id = order.id
        invoice.amount = form.amount.data
        invoice.date = datetime.utcnow()
        invoice.created_by = current_user.id
        invoice.created_at = datetime.utcnow()

        for item in order.order_items:
            _item = Item.query.get(item.item_id)
            if _item.category_id == 1:
                _item.quantity = _item.quantity - item.item_number
                db.session.commit()

        # payment done !!
        order.status = 2
        db.session.add(invoice)
        db.session.commit()
        flash('Enregistrement effectué!')
        return redirect(url_for('order.detail', id=id))
    form.amount.data = order.amount
    return render_template('order/detail.html',
                           order=order, title="order", form=form)


@bp.route('/order/validate/<int:id>', methods=['GET', 'POST'])
@login_required
def validate(id):
    form = ValidateForm()
    order = Order.query.get_or_404(id)
    if form.validate_on_submit():
        invoice = Invoice()
        invoice.serial = invoice_serial()
        invoice.order_id = order.id
        invoice.amount = form.amount.data
        invoice.date = datetime.utcnow()
        invoice.created_by = current_user.id
        invoice.created_at = datetime.utcnow()

        for item in order.order_items:
            _item = Item.query.get(item.item_id)
            if _item.category_id == 1:
                _item.quantity = _item.quantity - item.item_number
                db.session.commit()
        # payment done !!
        order.status = 2
        db.session.add(invoice)
        db.session.commit()
        flash('Enregistrement effectué!')
        return redirect(url_for('order.detail', id=id))
    form.amount.data = order.amount
    return render_template('order/detail.html',
                           order=order, title="order")


def invoice_serial():
    return "I" + datetime.utcnow().strftime("%Y%m%d%H%M%S")


def item_serial():
    return datetime.utcnow().strftime("%Y%m%d%H%M%S")
