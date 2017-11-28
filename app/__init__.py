from flask import Flask, render_template, url_for, jsonify, request
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.fileadmin import FileAdmin
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from glob import glob
from config import config, __APP_NAME__
import os.path as op

mail = Mail()
db = SQLAlchemy()
moment = Moment()
admin = Admin(name = __APP_NAME__ + ' Admin', template_mode="bootstrap3", url="/site/admin")
base_path = op.dirname(__file__)


def create_app(config_name):
    app = Flask(__name__, static_url_path='/staticsite')

    # add haml-like template syntax to jinja_env
    app.jinja_env.add_extension('hamlish_jinja.HamlishExtension')
    app.config.from_object(config[config_name])
    app.config['SECRET_KEY'] = 'Thatdumkey'
    config[config_name].init_app(app)

    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    admin.init_app(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # import custom filters for jinja templates
    from app.main.jinja_custom_filters import custom_filters
    app.jinja_env.filters = dict(app.jinja_env.filters, **custom_filters)

    return app
