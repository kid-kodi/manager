# app/Purchase/views.py
from datetime import datetime
from flask import abort, flash, redirect, request, render_template, url_for
from flask_login import current_user, login_required

from . import bp
from .forms import PurchaseForm, SearchForm, ValidateForm
from .. import db
from ..models import Purchase, Supplier, PurchaseItem, Item, Bill


# Purchase Views

@bp.route('/purchase', methods=['GET', 'POST'])
@login_required
def index():
    pagination = []
    search_form = SearchForm()
    page = request.args.get('page', 1, type=int)
    if search_form.validate_on_submit():
        name = search_form.name.data
        if name != '':
            pagination = Purchase.query.filter_by(name=name) \
                .order_by(Purchase.created_at.desc()).paginate(
                page, per_page=50,
                error_out=False)
        else:
            pagination = Purchase.query \
                .order_by(Purchase.created_at.desc()).paginate(
                page, per_page=50,
                error_out=False)
    else:
        pagination = Purchase.query \
            .order_by(Purchase.created_at.desc()).paginate(
            page, per_page=50,
            error_out=False)
    list = pagination.items
    return render_template('purchase/list.html',
                           list=list, pagination=pagination,
                           title="purchases", search_form=search_form)


@bp.route('/purchase/add', methods=['GET', 'POST'])
@login_required
def add():
    add = True
    form = PurchaseForm()
    form.supplier.choices = [(c.id, c.display_as) for c in Supplier.query.all()]
    for x in form.purchaseItems.entries:
        x.item_id.choices = [(c.id, c.name) for c in Item.query.all()]

    if form.validate_on_submit():
        purchase = Purchase(supplier_id=form.supplier.data,
                            serial=item_serial(),
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            send_date=form.send_date.data,
                            receive_date=form.receive_date.data,
                            amount=form.amount.data,
                            status=0,
                            created_by=current_user.id,
                            created_at=datetime.utcnow())
        db.session.add(purchase)
        db.session.commit()

        purchase_items = form.purchaseItems.entries
        for purchase_item in purchase_items:
            print(purchase_item.item_id.data)
            print(purchase_item.item_number.data)
            print(purchase_item.item_price.data)
            print(purchase_item.item_amount.data)
            purchase_item = PurchaseItem(purchase_id=purchase.id,
                                         item_id=purchase_item.item_id.data,
                                         item_number=purchase_item.item_number.data,
                                         item_price=purchase_item.item_price.data,
                                         item_amount=purchase_item.item_amount.data,
                                         created_by=current_user.id,
                                         created_at=datetime.utcnow())
            db.session.add(purchase_item)
            db.session.commit()

        flash('You have successfully saved the purchase.')

        # redirect to the bps page
        return redirect(url_for('purchase.index'))

    return render_template('purchase/form.html', action="Add",
                           add=add, form=form,
                           title="Add purchase")


@bp.route('/purchase/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    add = False
    purchase = Purchase.query.get_or_404(id)
    form = PurchaseForm(obj=purchase)
    form.supplier.choices = [(c.id, c.display_as) for c in Supplier.query.all()]
    for x in form.purchaseItems.entries:
        x.item_id.choices = [(c.id, c.name) for c in Item.query.all()]

    if form.validate_on_submit():
        purchase.supplier_id = form.supplier.data
        purchase.first_name = form.first_name.data
        purchase.last_name = form.last_name.data
        purchase.send_date = form.send_date.data
        purchase.receive_date = form.receive_date.data
        purchase.amount = form.amount.data
        purchase.purchase_items = []
        db.session.commit()
        purchase_items = form.purchaseItems.entries
        for purchase_item in purchase_items:
            _item = PurchaseItem(purchase_id=purchase.id,
                                 item_id=purchase_item.item_id.data,
                                 item_number=purchase_item.item_number.data,
                                 item_price=purchase_item.item_price.data,
                                 item_amount=purchase_item.item_amount.data)
            db.session.add(_item)
            db.session.commit()
        flash('You have successfully edited the purchase.')

        # redirect to the bps page
        return redirect(url_for('purchase.index'))

    form.supplier.data = purchase.supplier_id
    form.first_name.data = purchase.first_name
    form.last_name.data = purchase.last_name
    form.send_date.data = purchase.send_date
    form.receive_date.data = purchase.receive_date

    for purchase_item in purchase.purchase_items:
        form.purchaseItems.append_entry(purchase_item)

    for x in form.purchaseItems.entries:
        x.item_id.choices = [(c.id, c.name) for c in Item.query.all()]
    return render_template('purchase/form.html', action="Edit",
                           add=add, form=form,
                           purchase=purchase, title="Edit purchase")


@bp.route('/purchase/<int:id>', methods=['GET', 'POST'])
@login_required
def detail(id):
    form = ValidateForm()
    purchase = Purchase.query.get_or_404(id)
    if form.validate_on_submit():
        bill = Bill()
        bill.serial = bill_serial()
        bill.purchase_id = purchase.id
        bill.amount = form.amount.data
        bill.date = datetime.utcnow()
        bill.created_by = current_user.id
        bill.created_at = datetime.utcnow()

        for item in purchase.purchase_items:
            _item = Item.query.get(item.item_id)
            if _item.category_id == 1:
                _item.quantity = _item.quantity + item.item_number
                db.session.commit()

        # payment done !!
        purchase.status = 2
        db.session.add(bill)
        db.session.commit()
        flash('Enregistrement effectué!')
        return redirect(url_for('purchase.detail', id=id))
    form.amount.data = purchase.amount
    return render_template('purchase/detail.html',
                           purchase=purchase, title="purchase", form=form)


@bp.route('/purchase/validate/<int:id>', methods=['GET', 'POST'])
@login_required
def validate(id):
    form = ValidateForm()
    purchase = Purchase.query.get_or_404(id)
    if form.validate_on_submit():
        bill = Bill()
        bill.serial = bill_serial()
        bill.purchase_id = purchase.id
        bill.amount = form.amount.data
        bill.date = datetime.utcnow()
        bill.created_by = current_user.id
        bill.created_at = datetime.utcnow()
        # payment done !!
        purchase.status = 2
        db.session.add(bill)
        db.session.commit()
        flash('Enregistrement effectué!')
        return redirect(url_for('purchase.detail', id=id))
    form.amount.data = purchase.amount
    return render_template('purchase/detail.html',
                           purchase=purchase, title="purchase")


def bill_serial():
    return "F" + datetime.utcnow().strftime("%Y%m%d%H%M%S")


def item_serial():
    return datetime.utcnow().strftime("%Y%m%d%H%M%S")
