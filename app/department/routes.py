# app/department/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import department
from .forms import DepartmentForm
from .. import db
from ..models import Department

# Department Views

@department.route('/departments', methods=['GET', 'POST'])
@login_required
def list():
    """
    List all departments
    """

    list = Department.query.all()

    return render_template('department/list.html',
                           list=list, title="Departments")

@department.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add():
    """
    Add a department to the database
    """

    add = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('department.list'))

    # load department template
    return render_template('department/form.html', action="Add",
                           add=add, form=form,
                           title="Add Department")

@department.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """
    Edit a department
    """

    add = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the department.')

        # redirect to the departments page
        return redirect(url_for('department.list'))

    form.description.data = department.description
    form.name.data = department.name
    return render_template('department/form.html', action="Edit",
                           add=add, form=form,
                           department=department, title="Edit Department")

@department.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    """
    Delete a department from the database
    """

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('department.list'))