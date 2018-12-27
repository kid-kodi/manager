# app/spinneret/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import spinneret
from .forms import SpinneretForm
from .. import db
from ..models import Spinneret

# Spinneret Views

@spinneret.route('/spinnerets', methods=['GET', 'POST'])
@login_required
def list():
    """
    List all spinnerets
    """

    list = Spinneret.query.all()

    return render_template('spinneret/list.html',
                           list=list, title="Spinnerets")

@spinneret.route('/spinnerets/add', methods=['GET', 'POST'])
@login_required
def add():
    """
    Add a spinneret to the database
    """

    add = True

    form = SpinneretForm()
    if form.validate_on_submit():
        spinneret = Spinneret(name=form.name.data,
                                description=form.description.data)
        try:
            # add spinneret to the database
            db.session.add(spinneret)
            db.session.commit()
            flash('You have successfully added a new spinneret.')
        except:
            # in case spinneret name already exists
            flash('Error: spinneret name already exists.')

        # redirect to spinnerets page
        return redirect(url_for('spinneret.list'))

    # load spinneret template
    return render_template('spinneret/form.html', action="Add",
                           add=add, form=form,
                           title="Add Spinneret")

@spinneret.route('/spinnerets/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """
    Edit a spinneret
    """

    add = False

    spinneret = Spinneret.query.get_or_404(id)
    form = SpinneretForm(obj=spinneret)
    if form.validate_on_submit():
        spinneret.name = form.name.data
        spinneret.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the spinneret.')

        # redirect to the spinnerets page
        return redirect(url_for('spinneret.list'))

    form.description.data = spinneret.description
    form.name.data = spinneret.name
    return render_template('spinneret/form.html', action="Edit",
                           add=add, form=form,
                           spinneret=spinneret, title="Edit Spinneret")

@spinneret.route('/spinnerets/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    """
    Delete a spinneret from the database
    """

    spinneret = Spinneret.query.get_or_404(id)
    db.session.delete(spinneret)
    db.session.commit()
    flash('You have successfully deleted the spinneret.')

    # redirect to the spinnerets page
    return redirect(url_for('spinneret.list'))