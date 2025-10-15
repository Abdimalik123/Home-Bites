from datetime import datetime, timedelta
import functools
import os
import jwt
from dotenv import load_dotenv
from flask import Blueprint, jsonify, request, redirect, g
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from db import conn
load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"success": False, "error": "Missing or invalid token"}), 401

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"success": False, "error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"success": False, "error": "Invalid token"}), 401

        # Store user info in flask.g so routes can access it
        g.user = payload
        return view(*args, **kwargs)

    return wrapped_view

auth_bp = Blueprint('auth_bp', __name__)



@auth_bp.route('/register', methods = ['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        cursor = conn.cursor()

        if not firstname:
            return jsonify({ "success": False, "error": "Type in your first name"})
        if not lastname:
            return jsonify({ "success": False, "error": "Type in your last name"})
        if not email:
            return jsonify({ "success": False, "error": "Type in your email"})
        if not password:
            return jsonify({ "success": False, "error": "Type in your password"})
        if not confirm_password:
            return jsonify({ "success": False, "error": "Confirm your password"})
        if confirm_password != password:
            return jsonify({ "success": False, "error": "The passwords do not match"})
        
        
        try:
            cursor.execute("SELECT email FROM users WHERE email=%s", (email,))
            existing_email = cursor.fetchone()
            
            if existing_email:
                return jsonify({"success": False, "error": "Email already exists"})
            else:
                hashed_password = generate_password_hash(password)
                cursor.execute("INSERT INTO users (email, password_hash, first_name, last_name) VALUES (%s, %s, %s, %s) RETURNING id", (email, hashed_password, firstname, lastname))
                new_user_id = cursor.fetchone()[0]
                conn.commit()
                return jsonify({"success": True, "message": "Registration successful", "user_id": new_user_id})
        
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})
        finally:
            cursor.close()
        
    payload = {
            "user_id": new_user_id,
            "first_name": firstname,
            "last_name": lastname,
            "exp": int((datetime.utcnow() + timedelta(hours=24)).timestamp())
            }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')


    return {
        "success": True,
        "user": {
            "id": new_user_id,
            "first_name": firstname,
            "last_name": lastname,
            "email": email
        },
        "token": token
        }


@auth_bp.route('/login', methods = ['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    cursor = conn.cursor()

    if not email:
        return jsonify({ "success": False, "error": "Type in your email"})
    if not password:
        return jsonify({ "success": False, "error": "Type in your password"})
        
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user is None:
            return jsonify({ "success": False, "error": "Invalid credentials"}) 
               
        elif not check_password_hash(user[2], password):
                return jsonify({ "success": False, "error": "Invalid credentials"})
        else:
                payload = {
                    "user_id": user[0],
                    "first_name": user[4],
                    "last_name": user[5],
                    "exp": int((datetime.utcnow() + timedelta(hours=24)).timestamp())
                    }
                token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
                return jsonify( {
                    "success": True,
                    "user": {
                        "id": user[0],
                        "first_name": user[4],
                        "last_name": user[5],
                        "email": user[1]
                        },
                        "token": token
                        })
    except Exception as e:
        print("Login error:", e)
        return jsonify({ "success": False, "error": "Server error"}), 500
    finally:
        cursor.close()

