from flask import Blueprint
from routes.auth import login_required





comment_bp = Blueprint('comment_bp', __name__)