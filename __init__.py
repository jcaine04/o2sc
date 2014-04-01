from flask import Blueprint

o2sc = Blueprint('o2sc', __name__)

from . import views