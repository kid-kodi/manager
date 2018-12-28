# app/home/views.py
import os
from datetime import datetime
from flask import request, render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale

from app import db
from . import home
from ..models import User, Item, Unit, Department, Level, Spinneret
from .forms import EditProfileForm, ChangePasswordForm, SearchForm, ChangeAvatarForm

basedir = os.path.abspath(os.path.dirname(__file__))


@home.before_app_request
def before_request():
    users = User.query.all()
    number = len(users)
    # check if user exist in database
    if number == 0 and request.endpoint != 'setup.start' and request.endpoint != 'setup.company' and request.endpoint != 'setup.register':
        return redirect(url_for('setup.start'))
    elif current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@home.route('/')
@login_required
def dashboard():
    """
    Render the homepage template on the / route
    """
    user = User.query.all()
    item = Item.query.all()
    return render_template('home/index.html', user=user, item=item, title="Welcome")


@home.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@home.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('home.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


@home.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.password = form.password.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('home.user', username=current_user.username))
    return render_template('change_password.html', title=_('Change Password'),
                           form=form)


@home.route('/change_avatar', methods=['GET', 'POST'])
@login_required
def change_avatar():
    form = ChangeAvatarForm()
    if form.validate_on_submit():
        if 'image' in request.files:
            filename = images.save(request.files['image'])
            url = images.url(filename)
            print('file exist')
        else:
            print('file do not exist')
            filename = 'default.png'
            url = os.path.join(basedir, '/static/img/default.png')

        current_user.avatar = url
        db.session.commit()
        flash('You have successfully modifiy your avatar')
        return redirect(url_for('trainee.list'))

    # load trainee template
    return render_template('change_avatar.html',
                           form=form,
                           title="Add Trainee")


@home.route("/setup", methods=['GET', 'POST'])
@login_required
def setup():
    if request.method == 'POST':
        def department_init_func(row):
            d = Department(name=row['name'], description=row['description'])
            return d

        def unit_init_func(row):
            d = Department.query.filter_by(name=row['department']).first()
            u = Unit(name=row['name'], description=row['description'], department=d)
            return u

        def level_init_func(row):
            l = Level(name=row['name'], description=row['description'])
            return l

        def spinneret_init_func(row):
            s = Spinneret(name=row['name'], description=row['description'])
            return s

        def item_init_func(row):
            level = Level.query.filter_by(name=row['level']).first()
            unit = Unit.query.filter_by(name=row['unit']).first()
            spinneret = Spinneret.query.filter_by(name=row['spinneret']).first()
            c = Item()
            c.image_filename = 'default.png'
            c.image_url = os.path.join(basedir, 'app/static/img/trainee_default.png')
            c.registration_number = row['registration_number']
            c.first_name = row['first_name']
            c.last_name = row['last_name']
            c.level = level
            c.unit_id = unit
            c.spinneret = spinneret
            c.theme = row['theme']

            print(row)

        request.save_book_to_database(
            field_name='file', session=db.session,
            tables=[Department, Unit, Level, Spinneret, Item],
            initializers=[department_init_func, unit_init_func, level_init_func,
                          spinneret_init_func, item_init_func])
        return redirect(url_for('.handson_table'), code=302)
    return render_template('home/setup.html')


@home.route("/export", methods=['GET'])
@login_required
def doexport():
    return excel.make_response_from_tables(db.session, [Category, Post], "xls")


@home.route("/handson_view", methods=['GET'])
@login_required
def handson_table():
    return excel.make_response_from_tables(
        db.session, [Category, Post], 'home/handsontable.html')
