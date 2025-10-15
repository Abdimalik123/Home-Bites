from flask import Blueprint, redirect, session, url_for
from routes.auth import login_required




category_bp = Blueprint('category_bp', __name__)


category_bp.route('/', methods = ['GET'])
def all_categories():
    return "Coming soon"