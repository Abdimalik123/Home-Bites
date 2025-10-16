from flask import Blueprint, g, jsonify
from routes.auth import login_required
from db import conn




category_bp = Blueprint('category_bp', __name__)


@category_bp.route('/categories', methods = ['GET'])
def all_categories():
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM categories")
    rows = cursor.fetchall()
    cursor.close()
    categories = [row[0] for row in rows]
    return jsonify({"Categories": categories})

@category_bp.route('/categories/<int:category_id>/recipes', methods = ['GET'])
def get_recipes(category_id):
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT r.title, u.first_name, u.last_name FROM recipes r JOIN recipe_categories rc ON r.id = rc.recipe_id JOIN users u ON r.user_id = u.id WHERE rc.category_id = %s", (category_id,))
        all_recipe_info = cursor.fetchall()
        cursor.close()

        if not all_recipe_info:
            return jsonify({"message": "No recipes found for this category"}), 404
        
        info = [
            {
                "title":row[0],
                "firstname":row[1],
                "lastname":row[2]
            }
            for row in all_recipe_info
        ]
        return jsonify({"info": info}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500