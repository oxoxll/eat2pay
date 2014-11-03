from flask import Blueprint

clearing = Blueprint('clearing', __name__, static_folder='static')

from . import views


