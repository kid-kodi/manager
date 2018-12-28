# app/setup/views.py
import os
from datetime import datetime
from flask import flash, request, redirect, render_template, url_for, current_app
from flask_login import login_required, login_user, logout_user

from . import setup
from .forms import CompanyForm, RegistrationForm
from .. import db
from ..models import User, Company
from app import images
from flask_login import current_user


@setup.route('/start', methods=['GET', 'POST'])
def start():
    return render_template('setup/start.html')


@setup.route('/company', methods=['GET', 'POST'])
def company():
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
            url = os.path.join('', '/static/img/default.png')

        company = Company(registration_num=generateNum(),
                          logo=url,
                          phone=form.phone.data,
                          company_name=form.company_name.data,
                          email=form.email.data,
                          web_site=form.web_site.data,
                          address=form.address.data,
                          created_at=datetime.utcnow())
        db.session.add(company)
        db.session.commit()
        flash('You have successfully added a new company.')
        return redirect(url_for('setup.register', id=company.id))
    return render_template('setup/company.html', form=form, title='Login')


@setup.route('/register/<int:id>', methods=['GET', 'POST'])
def register(id):
    """
    Handle requests to the /register route
    Add an user to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(company_id=id,
                    avatar=os.path.join(current_app.config['UPLOADS_DEFAULT_DEST'], 'default.png'),
                    email=form.email.data,
                    username=form.username.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    password=form.password.data)

        # add user to the database
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('setup/register.html', form=form, title='Register')


def generateNum():
    now = datetime.utcnow()
    year = now.year
    number = str(year)[-2:] + 'ST-' + str(Company.query.count() + 1).zfill(4)
    return number
