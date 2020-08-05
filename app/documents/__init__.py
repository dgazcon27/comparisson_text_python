from flask import Blueprint

document_bp = Blueprint('document', __name__, template_folder='templates')

from . import routes