# app/models.py
import os
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from app import db, login

basedir = os.path.abspath(os.path.dirname(__file__))


class User(UserMixin, db.Model):
    """
    Create an User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    suppliers = db.relationship('Supplier', backref='user')
    orders = db.relationship('Order', backref='user')
    order_items = db.relationship('OrderItem', backref='user')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    avatar = db.Column(db.String, default=None, nullable=True)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


# Set up user_loader
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    units = db.relationship('Unit', backref='department',
                            lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)


class Unit(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'units'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    departement_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    trainees = db.relationship('Trainee', backref='unit',
                               lazy='dynamic')

    def __repr__(self):
        return '<Unit: {}>'.format(self.name)


class Spinneret(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'spinnerets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    trainees = db.relationship('Trainee', backref='spinneret')

    def __repr__(self):
        return '<Spinneret: {}>'.format(self.name)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_as = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    email = db.Column(db.String(255))
    description = db.Column(db.String(255))
    status = db.Column(db.Integer)
    orders = db.relationship('Order', backref='customer')
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Customer: {}>'.format(self.display_as)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    serial = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    send_date = db.Column(db.String(255))
    receive_date = db.Column(db.String(255))
    amount = db.Column(db.Integer)
    status = db.Column(db.Integer)
    order_items = db.relationship('OrderItem', backref='order')
    invoices = db.relationship('Invoice', backref='order')
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def balance(self):
        balance = self.amount
        invoices = self.invoices
        for invoice in invoices:
            balance = invoice.amount - balance
        return balance

    def paid(self):
        balance = 0
        invoices = self.invoices
        for invoice in invoices:
            balance = balance + invoice.amount
        return balance


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    item_amount = db.Column(db.Integer)
    item_number = db.Column(db.Integer)
    item_price = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))


# invoice for customer
class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    serial = db.Column(db.String(255))
    date = db.Column(db.String(255))
    amount = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))


# bill for suppliers

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    serial = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    send_date = db.Column(db.String(255))
    receive_date = db.Column(db.String(255))
    amount = db.Column(db.Integer)
    status = db.Column(db.Integer)
    purchase_items = db.relationship('PurchaseItem', backref='purchase')
    bills = db.relationship('Bill', backref='order')
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def balance(self):
        balance = self.amount
        bills = self.bills
        for bill in bills:
            balance = bill.amount - balance
        return balance

    def paid(self):
        balance = 0
        bills = self.bills
        for bill in bills:
            balance = balance + bill.amount
        return balance


class PurchaseItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    item_amount = db.Column(db.Integer)
    item_number = db.Column(db.Integer)
    item_price = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))


# invoice for customer
class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'))
    serial = db.Column(db.String(255))
    date = db.Column(db.String(255))
    amount = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))
    selling_price = db.Column(db.Integer)
    buying_price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    status = db.Column(db.Integer)
    order_items = db.relationship('OrderItem', backref='item')
    purchase_items = db.relationship('PurchaseItem', backref='item')
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_json(self):
        json_item = {
            'id': self.id,
            'category_id': self.category_id,
            'name': self.name,
            'description': self.description,
            'selling_price': self.selling_price,
            'buying_price': self.buying_price,
            'quantity': self.quantity,
            'status': self.status,
            'created_at': self.created_at,
            'created_by': self.created_by
        }
        return json_item

    def __repr__(self):
        return '<Item: {}>'.format(self.name)


class Level(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'levels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    description = db.Column(db.String(200))
    trainees = db.relationship('Trainee', backref='level')

    def __repr__(self):
        return '<Level: {}>'.format(self.name)


class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_as = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255))
    status = db.Column(db.Integer)
    purchases = db.relationship('Purchase', backref='supplier')
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Supplier: {}>'.format(self.name)


class Trainee(db.Model):
    __tablename__ = 'trainees'

    id = db.Column(db.Integer, primary_key=True)
    registration_number = db.Column(db.String)
    image_filename = db.Column(db.String, default=None, nullable=True)
    image_url = db.Column(db.String, default=None, nullable=True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    email = db.Column(db.String(60), index=True, unique=True)
    phone = db.Column(db.String(255), index=True, unique=True)
    birthdate = db.Column(db.String)
    school = db.Column(db.String)
    diplome = db.Column(db.String)
    spinneret_id = db.Column(db.Integer, db.ForeignKey('spinnerets.id'))
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'))
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'))
    responsable = db.Column(db.String)
    started_date = db.Column(db.String)
    ended_date = db.Column(db.String)
    apply_date = db.Column(db.String)
    theme = db.Column(db.String)
    status = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_json(self):
        json_trainee = {
            'id': self.id,
            'registration_number': self.registration_number,
            'image_filename': self.image_filename,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'birthdate': self.birthdate,
            'school': self.school,
            'diplome': self.diplome,
            'spinneret': self.spinneret.name,
            'level': self.level.name,
            'unit': self.unit.name,
            'responsable': self.responsable,
            'started_date': self.started_date,
            'ended_date': self.ended_date,
            'theme': self.theme
        }
        return json_trainee

    def __repr__(self):
        return '<Trainee: {}>'.format(self.first_name)


class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='role',
                            lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)


class Seed:
    @staticmethod
    def start():
        level_list = [
            Level(name='BTS', description=''),
            Level(name='MASTER', description=''),
            Level(name='MASTER2', description=''),
            Level(name='THESE D\'EXERCISE', description=''),
            Level(name='THESE UNIQUE', description='')]

        for lvl in level_list:
            db.session.add(lvl)
        db.session.commit()
