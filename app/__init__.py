from flask import Flask, render_template, url_for, jsonify, request
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from glob import glob
from config import config


mail = Mail()
#db = SQLAlchemy()
moment = Moment()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['SECRET_KEY'] = 'Rh1n0R4d10F0rm'
    config[config_name].init_app(app)

    mail.init_app(app)
    moment.init_app(app)
#    db.init_app(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
