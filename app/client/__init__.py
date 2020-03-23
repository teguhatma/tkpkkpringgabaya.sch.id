from flask import Blueprint

client = Blueprint("client", __name__, template_folder="templates")

from . import routes
