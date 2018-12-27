# app/Customer/views.py
from datetime import datetime
from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import bp
from .forms import CustomerForm
from .. import db
from ..models import Customer


# Customer Views

@bp.route('/customer', methods=['GET', 'POST'])
@login_required
def index():
    list = Customer.query.all()
    return render_template('customer/index.html',
                           list=list, title="customer")


@bp.route('/customer/add', methods=['GET', 'POST'])
@login_required
def add():
    add = True
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customer(
            display_as=form.display_as.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            email=form.email.data,
            description=form.description.data,
            status=1,
            created_by=current_user.id,
            created_at=datetime.utcnow())
        try:
            # add Customer to the database
            db.session.add(customer)
            db.session.commit()
            flash('Enregistrement effectué avec succès')
        except:
            # in case Customer name already exists
            flash('Cet élement figure deja dans votre base de donnée')

        # redirect to customer page
        return redirect(url_for('customer.index'))

    # load Customer template
    return render_template('customer/form.html', action="Add",
                           add=add, form=form,
                           title="Add Customer")


@bp.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    customer = Customer.query.get_or_404(id)
    form = CustomerForm(obj=customer)
    if form.validate_on_submit():
        customer.display_as = form.display_as.data
        customer.first_name = form.first_name.data
        customer.last_name = form.last_name.data
        customer.phone = form.phone.data
        customer.email = form.email.data
        customer.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the customer.')

        # redirect to the customers page
        return redirect(url_for('customer.index'))

    form.display_as.data = customer.display_as
    form.first_name.data = customer.first_name
    form.last_name.data = customer.last_name
    form.phone.data = customer.phone
    form.email.data = customer.email
    form.description.data = customer.description
    return render_template('customer/form.html', action="Edit", form=form, customer=customer, title="Edit Customer")


@bp.route('/customer/<int:id>', methods=['GET', 'POST'])
@login_required
def detail(id):
    customer = Customer.query.get_or_404(id)
    return render_template('customer/detail.html',
                           customer=customer, title="customer")


@bp.route('/customer/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    """
    Delete a Customer from the database
    """

    Customer = Customer.query.get_or_404(id)
    db.session.delete(Customer)
    db.session.commit()
    flash('You have successfully deleted the Customer.')

    # redirect to the customer page
    return redirect(url_for('Customer.list'))
