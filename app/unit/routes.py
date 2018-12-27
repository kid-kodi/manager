# app/unit/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import unit
from .forms import UnitForm
from .. import db
from ..models import Unit

# Unit Views

@unit.route('/units', methods=['GET', 'POST'])
@login_required
def list():
    """
    List all units
    """

    list = Unit.query.all()

    return render_template('unit/list.html',
                           list=list, title="Units")

@unit.route('/units/add', methods=['GET', 'POST'])
@login_required
def add():
    """
    Add a unit to the database
    """

    add = True

    form = UnitForm()
    if form.validate_on_submit():
        unit = Unit(name=form.name.data,
                                description=form.description.data)
        try:
            # add unit to the database
            db.session.add(unit)
            db.session.commit()
            flash('You have successfully added a new unit.')
        except:
            # in case unit name already exists
            flash('Error: unit name already exists.')

        # redirect to units page
        return redirect(url_for('unit.list'))

    # load unit template
    return render_template('unit/form.html', action="Add",
                           add=add, form=form,
                           title="Add Unit")

@unit.route('/units/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """
    Edit a unit
    """

    add = False

    unit = Unit.query.get_or_404(id)
    form = UnitForm(obj=unit)
    if form.validate_on_submit():
        unit.name = form.name.data
        unit.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the unit.')

        # redirect to the units page
        return redirect(url_for('unit.list'))

    form.description.data = unit.description
    form.name.data = unit.name
    return render_template('unit/form.html', action="Edit",
                           add=add, form=form,
                           unit=unit, title="Edit Unit")

@unit.route('/units/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    """
    Delete a unit from the database
    """

    unit = Unit.query.get_or_404(id)
    db.session.delete(unit)
    db.session.commit()
    flash('You have successfully deleted the unit.')

    # redirect to the units page
    return redirect(url_for('unit.list'))