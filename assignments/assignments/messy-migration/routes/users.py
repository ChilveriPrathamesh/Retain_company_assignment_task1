from flask import Blueprint, request, jsonify
from db import get_db_connection
from utils.security import hash_password, check_password
from schemas.user_schema import UserCreateSchema, UserUpdateSchema, LoginSchema
from marshmallow import ValidationError

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
def get_all_users():
    conn = get_db_connection()
    users = conn.execute('SELECT id, name, email FROM users').fetchall()
    conn.close()
    return jsonify([dict(user) for user in users]), 200

@users_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT id, name, email FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return jsonify(dict(user)), 200
    return jsonify({"error": "User not found"}), 404

@users_bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = UserCreateSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    conn = get_db_connection()
    hashed_pwd = hash_password(data['password'])

    conn.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
                 (data['name'], data['email'], hashed_pwd))
    conn.commit()
    conn.close()
    return jsonify({"message": "User created"}), 201

@users_bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = UserUpdateSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    if not data:
        return jsonify({"error": "No valid fields to update"}), 400

    conn = get_db_connection()
    query_parts = [f"{k} = ?" for k in data]
    query = f"UPDATE users SET {', '.join(query_parts)} WHERE id = ?"
    values = list(data.values()) + [user_id]

    conn.execute(query, tuple(values))
    conn.commit()
    conn.close()
    return jsonify({"message": "User updated"}), 200

@users_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"User {user_id} deleted"}), 200

@users_bp.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name', '')
    if not name:
        return jsonify({"error": "Missing name parameter"}), 400

    conn = get_db_connection()
    users = conn.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f'%{name}%',)).fetchall()
    conn.close()
    return jsonify([dict(user) for user in users]), 200

@users_bp.route('/login', methods=['POST'])
def login():
    try:
        data = LoginSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (data['email'],)).fetchone()
    conn.close()

    if user and check_password(data['password'], user['password']):
        return jsonify({"status": "success", "user_id": user['id']}), 200
    return jsonify({"status": "failed", "message": "Invalid credentials"}), 401
