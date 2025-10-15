from flask import Blueprint, g, jsonify
from routes.auth import login_required
from db import conn

fav_bp = Blueprint('fav_bp', __name__)


@fav_bp.route('/recipes/<int:recipe_id>/favorite', methods=['POST'])
@login_required
def add_to_favorite(recipe_id):
    user_id = g.user['user_id']
    cursor = conn.cursor()
    
    cursor.execute("SELECT 1 FROM favorites WHERE user_id = %s AND recipe_id = %s", (user_id, recipe_id))
    favorite = cursor.fetchone()

    if favorite:
        cursor.close()
        return jsonify({"message": "You have already added this recipe to favorites"}), 200

    cursor.execute("INSERT INTO favorites (user_id, recipe_id) VALUES (%s, %s)", (user_id, recipe_id))
    conn.commit()
    cursor.close()
    return jsonify({"message": "Recipe added to favorites"}), 201


@fav_bp.route('/recipes/<int:recipe_id>/favorite', methods=['DELETE'])
@login_required
def delete_favorite(recipe_id):
    user_id = g.user['user_id']
    cursor = conn.cursor()

    cursor.execute("DELETE FROM favorites WHERE user_id = %s AND recipe_id = %s", (user_id, recipe_id))
    
    if cursor.rowcount == 0:
        cursor.close()
        return jsonify({"message": "You haven't added this recipe to your favorites yet"}), 404

    conn.commit()
    cursor.close()
    return jsonify({"message": "You have removed this recipe from favorites"}), 200


@fav_bp.route('/favorites', methods=['GET'])
@login_required
def get_favorites():
    user_id = g.user['user_id']
    cursor = conn.cursor()

    cursor.execute("SELECT recipe_id FROM favorites WHERE user_id = %s", (user_id,))
    rows = cursor.fetchall()

    favorite_ids = [row[0] for row in rows]
    if not favorite_ids:
        cursor.close()
        return jsonify({"message": "You have no favorite recipes"}), 200

    placeholders = ','.join(['%s'] * len(favorite_ids))
    query = f"SELECT id, title, instructions FROM recipes WHERE id IN ({placeholders})"
    cursor.execute(query, favorite_ids)
    recipes = cursor.fetchall()

    recipe_list = [
        {"id": row[0], "title": row[1], "instructions": row[2]}
        for row in recipes
    ]

    cursor.close()
    return jsonify({"favorites": recipe_list}), 200
