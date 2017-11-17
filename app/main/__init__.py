from flask import Blueprint

main = Blueprint('main', __name__, url_prefix="/site")

from . import views, errors
