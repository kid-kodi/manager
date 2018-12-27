# app/level/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import level
from .forms import LevelForm
from .. import db
from ..models import Level

# Level Views

@level.route('/levels', methods=['GET', 'POST'])
@login_required
def list():
    """
    List all levels
    """

    list = Level.query.all()

    return render_template('level/list.html',
                           list=list, title="Levels")

@level.route('/levels/add', methods=['GET', 'POST'])
@login_required
def add():
    """
    Add a level to the database
    """

    add = True

    form = LevelForm()
    if form.validate_on_submit():
        level = Level(name=form.name.data,
                                description=form.description.data)
        try:
            # add level to the database
            db.session.add(level)
            db.session.commit()
            flash('You have successfully added a new level.')
        except:
            # in case level name already exists
            flash('Error: level name already exists.')

        # redirect to levels page
        return redirect(url_for('level.list'))

    # load level template
    return render_template('level/form.html', action="Add",
                           add=add, form=form,
                           title="Add Level")

@level.route('/levels/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """
    Edit a level
    """

    add = False

    level = Level.query.get_or_404(id)
    form = LevelForm(obj=level)
    if form.validate_on_submit():
        level.name = form.name.data
        level.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the level.')

        # redirect to the levels page
        return redirect(url_for('level.list'))

    form.description.data = level.description
    form.name.data = level.name
    return render_template('level/form.html', action="Edit",
                           add=add, form=form,
                           level=level, title="Edit Level")

@level.route('/levels/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    """
    Delete a level from the database
    """

    level = Level.query.get_or_404(id)
    db.session.delete(level)
    db.session.commit()
    flash('You have successfully deleted the level.')

    # redirect to the levels page
    return redirect(url_for('level.list'))