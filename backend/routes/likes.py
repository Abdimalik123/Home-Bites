from flask import Blueprint
from routes.auth import login_required
from db import conn





like_bp = Blueprint('like_bp', __name__)

@like_bp.route('/recipes/<id>/like', methods = ['POST'])
@login_required
def add_like():
    return "Coming soon"

@like_bp.route('/recipes/<id>/like', methods = ['DELETE'])
@login_required
def delete_like():
    return "Coming soon"

@like_bp.route('/recipes/<id>/likes', methods = ['GET'])
@login_required
def get_likes():
    return "Coming soon"