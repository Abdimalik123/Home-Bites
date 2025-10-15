from flask import Blueprint, Flask
from routes.auth import auth_bp 
from routes.recipes import recipe_bp
from routes.categories import category_bp
from routes.comments import comment_bp
from routes.favorites import fav_bp
from routes.likes import like_bp
from db import conn
import os
from flask_cors import CORS





app = Flask(__name__)
CORS(app)
app.register_blueprint(auth_bp)
app.register_blueprint(recipe_bp)
app.register_blueprint(category_bp)
app.register_blueprint(comment_bp)
app.register_blueprint(fav_bp)
app.register_blueprint(like_bp)



if __name__ == "__main__":
    app.secret_key = os.getenv("SECRET_KEY")
    app.run(host="0.0.0.0", port=5000, debug=True)








