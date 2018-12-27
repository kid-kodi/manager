# app/Supplier/views.py
from datetime import datetime
from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import bp
from .forms import SupplierForm
from .. import db
from ..models import Supplier


# Supplier Views

@bp.route('/supplier', methods=['GET', 'POST'])
@login_required
def index():
    list = Supplier.query.all()
    return render_template('supplier/index.html',
                           list=list, title="supplier")


@bp.route('/supplier/add', methods=['GET', 'POST'])
@login_required
def add():
    add = True
    form = SupplierForm()
    if form.validate_on_submit():
        supplier = Supplier(
            display_as=form.display_as.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            email=form.email.data,
            status=1,
            created_by=current_user.id,
            created_at=datetime.utcnow())
        try:
            # add Supplier to the database
            db.session.add(supplier)
            db.session.commit()
            flash('Enregistrement effectué avec succès')
        except:
            # in case Supplier name already exists
            flash('Cet élement figure deja dans votre base de donnée')

        # redirect to supplier page
        return redirect(url_for('supplier.index'))

    # load Supplier template
    return render_template('supplier/form.html', action="Add",
                           add=add, form=form,
                           title="Add Supplier")


@bp.route('/supplier/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    supplier = Supplier.query.get_or_404(id)
    form = SupplierForm(obj=Supplier)
    if form.validate_on_submit():
        supplier.display_as = form.display_as.data
        supplier.first_name = form.first_name.data
        supplier.last_name = form.last_name.data
        supplier.phone = form.phone.data
        supplier.email = form.email.data
        db.session.commit()
        flash('Modifications effectuées avec succès')

        # redirect to the supplier page
        return redirect(url_for('supplier.index'))

    form.display_as.data = supplier.display_as
    form.first_name.data = supplier.first_name
    form.last_name.data = supplier.last_name
    form.phone.data = supplier.phone
    form.email.data = supplier.email
    return render_template('supplier/form.html', action="Edit",add=add, form=form,supplier=supplier, title="Edit Supplier")


@bp.route('/supplier/<int:id>', methods=['GET', 'POST'])
@login_required
def detail(id):
    supplier = Supplier.query.get_or_404(id)
    return render_template('supplier/detail.html',
                           supplier=supplier, title="supplier")


@bp.route('/supplier/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    """
    Delete a Supplier from the database
    """

    Supplier = Supplier.query.get_or_404(id)
    db.session.delete(Supplier)
    db.session.commit()
    flash('You have successfully deleted the Supplier.')

    # redirect to the supplier page
    return redirect(url_for('Supplier.list'))
