from flask import Blueprint, g, jsonify, redirect, request, session, url_for
from routes.auth import login_required
from db import conn


recipe_bp = Blueprint('recipe_bp', __name__)




@recipe_bp.route('/', methods = ['GET'])
def home():
    return "Coming soon"


@recipe_bp.route('/recipes', methods = ['GET'])
def all_recipes():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            r.id AS recipe_id,
            u.first_name, 
            u.last_name, 
            r.title, 
            r.instructions, 
            r.created_at, 
            i.name AS ingredient_name, 
            ri.quantity, 
            ri.unit
        FROM users u
        JOIN recipes r ON u.id = r.user_id
        JOIN recipe_ingredients ri ON r.id = ri.recipe_id
        JOIN ingredient_master i ON ri.ingredient_id = i.id
    """)
    rows = cursor.fetchall()
    cursor.close()

    recipes_dict = {}
    for row in rows:
        recipe_id, first_name, last_name, title, instructions, created_at, ingredient_name, quantity, unit = row
        
        if recipe_id not in recipes_dict:
            recipes_dict[recipe_id] = {
                "recipe_id": recipe_id,
                "author": {"first_name": first_name, "last_name": last_name},
                "title": title,
                "instructions": instructions,
                "created_at": created_at,
                "ingredients": []
            }
        
        recipes_dict[recipe_id]["ingredients"].append({
            "name": ingredient_name,
            "quantity": quantity,
            "unit": unit
        })

    # Convert to list
    data = list(recipes_dict.values())
    return jsonify(data)




@recipe_bp.route('/recipes/<int:recipe_id>', methods = ['GET'] )
@login_required
def view_recipe(recipe_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            r.id AS recipe_id,
            u.first_name, 
            u.last_name, 
            r.title, 
            r.instructions, 
            r.created_at, 
            i.name AS ingredient_name, 
            ri.quantity, 
            ri.unit
        FROM users u
        JOIN recipes r ON u.id = r.user_id
        JOIN recipe_ingredients ri ON r.id = ri.recipe_id
        JOIN ingredient_master i ON ri.ingredient_id = i.id
        WHERE r.id = %s
                   """, (recipe_id,))
    
    rows = cursor.fetchall()
    if not rows:
        return jsonify({"error":"Recipe not found"}), 404
    

    first_row = rows[0]
    recipe_data = {
        "recipe_id": first_row[0],
        "author": {"first_name": first_row[1], "last_name": first_row[2]},
        "title": first_row[3],
        "instructions": first_row[4],
        "created_at": first_row[5],
        "ingredients": []
    }

    # Append all ingredients
    for row in rows:
        ingredient_name, quantity, unit = row[6], row[7], row[8]
        recipe_data["ingredients"].append({
            "name": ingredient_name,
            "quantity": quantity,
            "unit": unit
        })

    return jsonify(recipe_data)

@recipe_bp.route('/recipes', methods = ['POST'] )
#login_required
def create_recipe():
    # Get JSON data from frontend
    data = request.get_json()
    
    # Extract fields
    title = data.get('title')
    instructions = data.get('instructions')
    ingredients = data.get('ingredients', [])
    categories = data.get('categories', [])
    
    # Validate required fields
    if not title or not instructions:
        return jsonify({"error": "Title and instructions are required"}), 400
    
    # Get current user ID from session
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401
    
    try:
        cursor = conn.cursor()
        
        # Insert recipe (only title and instructions based on your schema)
        cursor.execute("""
            INSERT INTO recipes (user_id, title, instructions)
            VALUES (%s, %s, %s)
        """, (user_id, title, instructions))
        
        # Get the ID of the newly created recipe
        recipe_id = cursor.lastrowid
        
        # Insert ingredients if provided
        # Note: Your schema uses ingredient_master table with ingredient_id
        for ingredient in ingredients:
            ingredient_name = ingredient.get('name')
            quantity = ingredient.get('quantity')
            unit = ingredient.get('unit')
            
            if ingredient_name and quantity:
                # First, check if ingredient exists in ingredient_master
                cursor.execute("""
                    SELECT id FROM ingredient_master WHERE name = %s
                """, (ingredient_name,))
                result = cursor.fetchone()
                
                if result:
                    ingredient_id = result[0]
                else:
                    # Insert new ingredient into master table
                    cursor.execute("""
                        INSERT INTO ingredient_master (name) VALUES (%s)
                    """, (ingredient_name,))
                    ingredient_id = cursor.lastrowid
                
                # Insert into recipe_ingredients
                cursor.execute("""
                    INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit)
                    VALUES (%s, %s, %s, %s)
                """, (recipe_id, ingredient_id, quantity, unit))
        
        # Insert categories if provided
        for category_name in categories:
            if category_name:
                # Check if category exists in categories table
                cursor.execute("""
                    SELECT id FROM categories WHERE name = %s
                """, (category_name,))
                result = cursor.fetchone()
                
                if result:
                    category_id = result[0]
                else:
                    # Insert new category into categories table
                    cursor.execute("""
                        INSERT INTO categories (name) VALUES (%s)
                    """, (category_name,))
                    category_id = cursor.lastrowid
                
                # Link recipe to category
                cursor.execute("""
                    INSERT INTO recipe_categories (recipe_id, category_id)
                    VALUES (%s, %s)
                """, (recipe_id, category_id))
        
        # Commit the transaction
        conn.commit()
        cursor.close()
        
        return jsonify({
            "message": "Recipe created successfully",
            "recipe_id": recipe_id
        }), 201
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Failed to create recipe: {str(e)}"}), 500

@recipe_bp.route('/recipes/<int:recipe_id>', methods = ['PUT'] )
@login_required
def edit_recipe(recipe_id):
    # Get JSON data from frontend
    data = request.get_json()
    
    # Extract fields
    new_title = data.get('title')
    new_instructions = data.get('instructions')
    new_ingredients = data.get('ingredients', [])
    new_categories = data.get('categories', [])
    
    # Validate required fields
    if not new_title or not new_instructions:
        return jsonify({"error": "Title and instructions are required"}), 400
    
    # Get current user ID from session
    user_id = g.user['user_id']

    try:
        cursor= conn.cursor()

        cursor.execute("SELECT user_id FROM recipes WHERE id = %s", (recipe_id))
        recipe_owner_id = cursor.fetchone()[0]

        if user_id != recipe_owner_id:
            return jsonify({"error": "Unauthorized"}), 403
        else:
            cursor.execute("UPDATE recipes SET title = %s, instructions = %s WHERE id = %s", (new_title, new_instructions, recipe_id))
            cursor.execute("DELETE FROM recipe_ingredients WHERE recipe_id = %s", (recipe_id))
            cursor.execute("DELETE FROM recipe_categories WHERE recipe_id = %s", (recipe_id))
            for ingredient in new_ingredients:
                ingredient_name = ingredient.get('name')
                quantity = ingredient.get('quantity')
                unit = ingredient.get('unit')
                
                if ingredient_name and quantity:
                    # First, check if ingredient exists in ingredient_master
                    cursor.execute("""
                        SELECT id FROM ingredient_master WHERE name = %s
                    """, (ingredient_name,))
                    result = cursor.fetchone()
                    
                    if result:
                        ingredient_id = result[0]
                    else:
                        # Insert new ingredient into master table
                        cursor.execute("""
                            INSERT INTO ingredient_master (name) VALUES (%s)
                        """, (ingredient_name,))
                        ingredient_id = cursor.lastrowid
                    
                    # Insert into recipe_ingredients
                    cursor.execute("""
                        INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit)
                        VALUES (%s, %s, %s, %s)
                    """, (recipe_id, ingredient_id, quantity, unit))
            for category_name in new_categories:
                if category_name:
                    # Check if category exists in categories table
                    cursor.execute("""
                        SELECT id FROM categories WHERE name = %s
                    """, (category_name,))
                    result = cursor.fetchone()
                    
                    if result:
                        category_id = result[0]
                    else:
                        # Insert new category into categories table
                        cursor.execute("""
                            INSERT INTO categories (name) VALUES (%s)
                        """, (category_name,))
                        category_id = cursor.lastrowid
                    
                    # Link recipe to category
                    cursor.execute("""
                        INSERT INTO recipe_categories (recipe_id, category_id)
                        VALUES (%s, %s)
                    """, (recipe_id, category_id))
        
        # Commit the transaction
        conn.commit()
        cursor.close()
        
        return jsonify({
            "message": "Recipe edited successfully",
            "recipe_id": recipe_id
        }), 201
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Failed to edit recipe: {str(e)}"}), 500




@recipe_bp.route('/recipes/<int:recipe_id>', methods = ['DELETE'] )
@login_required
def delete_recipe(recipe_id):
    
    cursor= conn.cursor()
    user_id = g.user['user_id']
    cursor.execute("SELECT user_id FROM recipes WHERE id = %s", (recipe_id))
    recipe_owner_id = cursor.fetchone()[0]

    try:
        if user_id != recipe_owner_id:
            return jsonify({"error": "Unauthorized"}), 403
        else:
            cursor.execute("DELETE FROM recipe_ingredients WHERE recipe_id = %s", (recipe_id))
            cursor.execute("DELETE FROM recipe_categories WHERE recipe_id = %s", (recipe_id))
            cursor.execute("DELETE FROM recipes WHERE id = %s", (recipe_id,))
            conn.commit()
            cursor.close()
    
        return jsonify({
            "message": "Recipe deleted successfully",
            "recipe_id": recipe_id
        }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Failed to delete recipe: {str(e)}"}), 500