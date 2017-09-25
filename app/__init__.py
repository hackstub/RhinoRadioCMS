from flask import Flask, render_template, url_for, jsonify, request
from flask_mail import Mail
from flask_admin import Admin
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from glob import glob
from config import config


mail = Mail()
db = SQLAlchemy()
moment = Moment()
admin = Admin(name='Radio Rhino', template_mode="bootstrap3")

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['SECRET_KEY'] = 'Thatdumkey'
    config[config_name].init_app(app)

    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    admin.init_app(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
