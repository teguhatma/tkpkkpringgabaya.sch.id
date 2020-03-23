from flask import Blueprint

murid = Blueprint("murid", __name__, template_folder="templates")

from . import routes
