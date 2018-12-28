# app/__init__.py

# third-party imports
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads

import flask_excel as excel
from elasticsearch import Elasticsearch
from flask_babel import Babel, lazy_gettext as _l

# local imports
from config import Config

db = SQLAlchemy()
login = LoginManager()
babel = Babel()
images = UploadSet('images', IMAGES)


def create_app(config_name=Config):
    app = Flask(__name__)
    app.config.from_object(config_name)

    Bootstrap(app)
    db.init_app(app)
    login.init_app(app)
    login.login_message = "You must be logged in to access this page."
    login.login_view = "auth.login"
    migrate = Migrate(app, db)
    excel.init_excel(app)
    configure_uploads(app, images)
    babel.init_app(app)
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    from app import models

    from .department import department as department_blueprint
    app.register_blueprint(department_blueprint)

    from .unit import unit as unit_blueprint
    app.register_blueprint(unit_blueprint)

    from .role import role as role_blueprint
    app.register_blueprint(role_blueprint)

    from .setup import setup as setup_blueprint
    app.register_blueprint(setup_blueprint)

    from .company import company as company_blueprint
    app.register_blueprint(company_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .supplier import bp as supplier_blueprint
    app.register_blueprint(supplier_blueprint)

    from .item import bp as item_blueprint
    app.register_blueprint(item_blueprint)

    from .customer import bp as customer_blueprint
    app.register_blueprint(customer_blueprint)

    from .order import bp as order_blueprint
    app.register_blueprint(order_blueprint)

    from .purchase import bp as purchase_blueprint
    app.register_blueprint(purchase_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    from .level import level as level_blueprint
    app.register_blueprint(level_blueprint)

    from .spinneret import spinneret as spinneret_blueprint
    app.register_blueprint(spinneret_blueprint)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1.0')

    from app.report import bp as report_bp
    app.register_blueprint(report_bp)

    return app
