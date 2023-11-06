from flask import Blueprint

bp = Blueprint('document', __name__)

from app.documents import routes
