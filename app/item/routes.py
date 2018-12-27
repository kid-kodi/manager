# app/Item/views.py
from datetime import datetime
from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import bp
from .forms import ItemForm
from .. import db
from ..models import Item


# Item Views

@bp.route('/item', methods=['GET', 'POST'])
@login_required
def list():
    list = Item.query.all()
    return render_template('item/list.html',
                           list=list, title="item")


@bp.route('/item/add', methods=['GET', 'POST'])
@login_required
def add():
    add = True
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(category_id=form.category.data,
                    name=form.name.data,
                    description=form.description.data,
                    selling_price=form.selling_price.data,
                    buying_price=form.buying_price.data,
                    quantity=form.quantity.data,
                    status=1,
                    created_by=current_user.id,
                    created_at=datetime.utcnow())
        try:
            # add Item to the database
            db.session.add(item)
            db.session.commit()
            flash('Enregistrement effectué avec succès')
        except:
            # in case Item name already exists
            flash('Cet élement figure déja dans votre base de donnée')

        # redirect to item page
        return redirect(url_for('item.list'))

    # load Item template
    return render_template('item/form.html', action="Add",
                           add=add, form=form,
                           title="Add Item")


@bp.route('/item/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    item = Item.query.get_or_404(id)
    form = ItemForm(obj=Item)
    if form.validate_on_submit():
        item.category_id = form.category.data
        item.name = form.name.data
        item.description = form.description.data
        item.selling_price = form.selling_price.data
        item.quantity = form.quantity.data
        item.status = 1
        item.buying_price = form.buying_price.data
        db.session.commit()
        flash('Modifications effectuées avec succès')

        # redirect to the item page
        return redirect(url_for('item.list'))

    form.name.data = item.name
    form.description.data = item.description
    form.selling_price.data = item.selling_price
    form.buying_price.data = item.buying_price
    form.quantity.data = item.quantity
    form.category.data = item.category_id
    return render_template('item/form.html', action="Edit",
                           add=add, form=form,
                           item=item, title="Edit Item")


@bp.route('/item/<int:id>', methods=['GET', 'POST'])
@login_required
def detail(id):
    item = Item.query.get_or_404(id)
    return render_template('item/detail.html',
                           item=item, title="item")


@bp.route('/item/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    Item = Item.query.get_or_404(id)
    db.session.delete(Item)
    db.session.commit()
    flash('You have successfully deleted the Item.')
    # redirect to the item page
    return redirect(url_for('item.list'))
