from flask import Blueprint, g, jsonify
from routes.auth import login_required
from db import conn

like_bp = Blueprint('like_bp', __name__)

@like_bp.route('/recipes/<int:recipe_id>/like', methods = ['POST'])
@login_required
def add_like(recipe_id):
    user_id = g.user['user_id']
    cursor = conn.cursor()
    
    #Check if like exists
    cursor.execute("SELECT 1 FROM likes WHERE user_id = %s AND recipe_id = %s", (user_id, recipe_id))
    like = cursor.fetchone()

    if like:
        return jsonify({"message": "You have already liked this recipe"})
    # Insert into database if like does not exist
    else:
        cursor.execute("INSERT INTO likes (user_id, recipe_id) VALUES (%s, %s)", (user_id, recipe_id))
        conn.commit()
        return jsonify({"message": "Recipe liked successfully"}), 201

@like_bp.route('/recipes/<int:recipe_id>/like', methods = ['DELETE'])
@login_required
def delete_like(recipe_id):
    user_id = g.user['user_id']
    cursor = conn.cursor()

    cursor.execute("DELETE FROM likes WHERE user_id = %s AND recipe_id = %s", (user_id, recipe_id))
    
    if cursor.rowcount == 0:
        return jsonify({"message": "You havent't liked this recipe"}), 404
    else:
        conn.commit()
        return jsonify({"message": "You have unliked this recipe"})
  

@like_bp.route('/recipes/<int:recipe_id>/likes', methods = ['GET'])
@login_required
def get_likes(recipe_id):
    cursor = conn.cursor()

    # Get all likes for this recipe
    cursor.execute("SELECT COUNT(user_id) FROM likes WHERE recipe_id = %s", (recipe_id,))
    like_count = cursor.fetchone()[0]

    return jsonify({"recipe_id": recipe_id, "like_count": like_count})
