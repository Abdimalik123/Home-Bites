from flask import Blueprint, g, jsonify, request
from routes.auth import login_required
from db import conn
comment_bp = Blueprint('comment_bp', __name__)




@comment_bp.route('/recipes/<int:recipe_id>/comment', methods = ['POST'])
@login_required
def add_comment(recipe_id):
    data = request.get_json()
    text = data.get("text")
    rating = data.get("rating")

    if not text or not rating:
        return jsonify({"error": "Text and rating is required"}), 400

    user_id = g.user['user_id']
    if not user_id:
        return jsonify({"error": "User nnot authenticated"})
    
    cursor = conn.cursor()
    #Insert comment
    cursor.execute("INSERT INTO comments (user_id, recipe_id, text, rating) VALUES (%s, %s, %s, %s)", (user_id, recipe_id, text, rating))
    conn.commit()
    cursor.close()
    return jsonify({"message": "Comment added successfully"})





@comment_bp.route('/recipes/<int:recipe_id>/comment', methods = ['GET'])
@login_required
def get_comments(recipe_id):
    cursor = conn.cursor()
    cursor.execute("SELECT u.first_name, u.last_name, c.text, c.rating, c.created_at FROM comments c JOIN users u ON u.id = c.user_id WHERE c.recipe_id = %s" , (recipe_id,))
    rows = cursor.fetchall()

    comments = [
        {
        "first_name": row[0],
        "last_name": row[1],
        "text": row[2],
        "rating": row[3],
        "created_at": row[4].isoformat()
        }
        for row in rows
    ]
    return jsonify({"comments": comments})



@comment_bp.route('/comments/<int:comment_id>', methods = ['DELETE'])
@login_required
def delete_comment(comment_id):
    user_id = g.user['user_id']
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM comments WHERE id = %s", (comment_id))
    result= cursor.fetchone()

    if result is None:
        return jsonify({"error": "Comment not found"}), 404
    
    comment_user_id = result[0]

    if comment_user_id != user_id:
        return jsonify({"error": "Unauthorized attempt"}), 403
    
    cursor.execute("DELETE FROM comments WHERE id = %s", (comment_id))
    conn.commit()
    cursor.close()
    return jsonify({"message":"Comment deleted successfully"}), 200
  