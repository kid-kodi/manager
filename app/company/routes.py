# app/company/views.py
import os
from flask import abort, flash, request, redirect, render_template, url_for, jsonify
# from flask_weasyprint import HTML, render_pdf
from flask_login import current_user, login_required

from . import company
from .forms import CompanyForm, SearchForm
from .. import db, images
from ..models import Company, Level, Spinneret, Unit, User, Department

import flask_excel as excel
from datetime import datetime
from flask_weasyprint import HTML, render_pdf

basedir = ''

from sqlalchemy.sql.expression import and_


def get_query(table, lookups, form_data):
    conditions = [
        getattr(table, field_name) == form_data[field_name]
        for field_name in lookups if form_data[field_name]
    ]

    return table.query.filter(and_(*conditions))


# routes order
@company.route('/company', methods=['GET', 'POST'])
@login_required
def list():
    page = request.args.get('page', 1, type=int)
    form = SearchForm()
    if form.validate_on_submit():
        company_name = form.company_name.data
        email = form.email.data
        phone = form.phone.data
        query = Company.query
        if company_name:
            query = query.filter(Company.company_name == company_name)
        elif email:
            query = query.filter(Company.email == email)
        elif phone > 0:
            query = query.filter(Company.phone == phone)

        pagination = query.order_by(Company.created_at.desc()).paginate(
            page, per_page=25,
            error_out=False)
    else:
        pagination = Company.query.order_by(Company.created_at.desc()).paginate(
            page, per_page=25,
            error_out=False)

    _list = pagination.items
    return render_template('company/list.html', list=_list, form=form, pagination=pagination)


@company.route('/company/add', methods=['GET', 'POST'])
@login_required
def add():
    """
    Add a company to the database
    """

    add = True

    form = CompanyForm()
    form.registration_number.data = "#"
    if form.validate_on_submit():
        if 'image' in request.files:
            filename = images.save(request.files['image'])
            url = images.url(filename)
            print('file exist')
        else:
            print('file do not exist')
            filename = 'default.png'
            url = os.path.join(basedir, '/static/img/default.png')

        company = Company(registration_number=generateNum(),
                          logo=url,
                          phone=form.phone.data,
                          company_name=form.company_name.data,
                          email=form.email.data,
                          web_site=form.web_site.data,
                          address=form.address.data,
                          created_at=datetime.utcnow(),
                          created_by=current_user.id)
        try:
            # add company to the database
            db.session.add(company)
            db.session.commit()
            flash('You have successfully added a new company.')
        except:
            # in case company name already exists
            flash('Error: company name already exists.')

        # redirect to company page
        return redirect(url_for('company.list'))

    # load company template
    return render_template('company/form.html', action="Add",
                           add=add, form=form,
                           title="Add Company")


@company.route('/company/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    company = Company.query.get_or_404(id)
    form = CompanyForm(obj=company)
    if form.validate_on_submit():
        if 'image' in request.files:
            filename = images.save(request.files['image'])
            url = images.url(filename)
            company.logo = url

        company.phone = form.phone.data
        company.company_name = form.company_name.data
        company.web_site = form.web_site.data
        company.email = form.email.data
        company.address = form.address.data
        db.session.commit()
        flash('You have successfully edited the company.')

        # redirect to the company page
        return redirect(url_for('company.list'))

    form.phone.data = company.phone
    form.web_site.data = company.web_site
    form.company_name.data = company.company_name
    form.email.data = company.email
    return render_template('company/form.html', action="Edit",
                           add=add, form=form,
                           company=company, title="Edit Company")


@company.route('/company/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    """
    Delete a company from the database
    """

    company = Company.query.get_or_404(id)
    db.session.delete(company)
    db.session.commit()
    flash('You have successfully deleted the company.')

    # redirect to the company page
    return redirect(url_for('company.list'))


@company.route("/company/import", methods=['GET', 'POST'])
@login_required
def import_in():
    if request.method == 'POST':

        def level_init(row):
            l = Level()
            num = Level.query.filter_by(name=row['Nom']).count()
            if num == 0:
                l.name = row['Nom']
                l.description = row['Description']
            return l

        def spinneret_init(row):
            s = Spinneret()
            num = Spinneret.query.filter_by(name=row['Nom']).count()
            if num == 0:
                s.name = row['Nom']
                s.description = row['Description']
            return s

        def department_init(row):
            s = Department()
            num = Department.query.filter_by(name=row['Nom']).count()
            print(str(num))
            if num == 0:
                s.name = row['Nom']
                s.description = row['Description']
            return s

        def unit_init(row):
            s = Unit()
            num = Unit.query.filter_by(name=row['Nom']).count()
            if num == 0:
                s.name = row['Nom']
                s.description = row['Description']
                d = Department.query.filter_by(name=row['Departement']).first()
                s.departement_id = d.id
            return s

        def company_init(row):
            c = Company()
            c.image_filename = 'default.png'
            c.image_url = os.path.join('', '/static/img/default.png')
            c.registration_number = row['Numero']
            c.company_name = row['Nom']
            c.email = row['Prenoms']

            l = Level.query.filter_by(name=row['Niveau']).first()
            c.level_id = l.id

            u = Unit.query.filter_by(name=row['Unite']).first()
            c.phone = u.id

            s = Spinneret.query.filter_by(name=row['Filiere']).first()
            c.spinneret_id = s.id

            c.school = row['Etablissement']
            c.email = row['Email']
            c.phone = row['Telephone']
            c.birthdate = row['Date de naissance']
            c.diplome = row['Diplome']
            c.theme = row['Theme']
            c.started_date = row['Date de debut de stage']
            c.ended_date = row['Date de fin de stage']
            c.responsable = row['Responsable']
            return c

        request.save_book_to_database(
            field_name='file', session=db.session,
            tables=[Department, Unit, Spinneret, Level, Company],
            initializers=[department_init, unit_init, spinneret_init, level_init, company_init])
        return redirect(url_for('company.list'))
    return render_template('company/import.html', company=company)


@company.route("/company/export", methods=['GET'])
@login_required
def export_out():
    list = Company.query.all()
    column_names = ['registration_number', 'company_name', 'email', 'level_id', 'phone',
                    'school', 'email', 'phone', 'theme']
    return excel.make_response_from_query_sets(list, column_names, "xls", file_name="company_data")


@company.route("/company/download", methods=['GET'])
@login_required
def download():
    return excel.make_response_from_array([['registration_number', 'company_name', 'email', 'level_id', 'phone',
                                            'school', 'email', 'phone', 'theme']],
                                          "xls", file_name="company_samples")


@company.route('/company/print', methods=['GET', 'POST'])
@login_required
def print_to():
    data = request.get_json()
    ids = data['items']
    print(data['items'])
    company = Company.query.filter(Company.id.in_(ids)).all()
    for value in company:
        print(value)
    # Make a PDF straight from HTML in a string.
    return jsonify({'company': [company.to_json() for company in company]})


@company.route('/company/pdf', methods=['GET', 'POST'])
@login_required
def pdf():
    name = 'kone'
    # Make a PDF straight from HTML in a string.
    html = render_template('company/pdf.html', name=name)
    return render_pdf(HTML(string=html))


def generateNum():
    now = datetime.utcnow()
    year = now.year
    number = str(year)[-2:] + 'ST-' + str(Company.query.count() + 1).zfill(4)
    return number
