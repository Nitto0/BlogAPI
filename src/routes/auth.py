from src import create_app
from flask import request, jsonify
from pydantic import ValidationError

from src.schemas.user import UserSchema
from src.models.user import User
from src.extensions import db

app = create_app()


@app.route("/api/v1/auth/register", methods=["POST"])
def register():
    data = request.json

    if not data:
        return jsonify({
            "error": {
                "code": "invalid_json",
                "message": "Incorrect data"
            }
        }), 400

    if 'username' not in data or 'password' not in data or 'email' not in data:
        return jsonify({
            "error": {
                "code": "invalid_json",
                "message": "Incorrect data!"
            }
        }), 400

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    try:
        validate_reg = UserSchema(username=username, password=password, email=email)

        print(f'''
                Success validation!
                Username: {validate_reg.username},
                password: {validate_reg.password},
                email: {validate_reg.email}
            ''')
    except ValidationError:
        return jsonify({
            "error": {
                "code": "validation_error",
                "message": "Invalid data!"
            }
        }), 422

    email = email.strip().lower()
    username = username.strip().lower()

    existing_user = db.session.execute(
        db.select(User).where(
            (User.email == email) | (User.username == username)
        )
    ).scalar_one_or_none()

    if existing_user:
        if existing_user.email == email:
            return jsonify({
                "error": {
                    "code": "email_already_exists",
                    "message": "Email already exists"
                }
            }), 409

        if existing_user.username == username:
            return jsonify({
                "error": {
                    "code": "username_already_exists",
                    "message": "Username already exists"
                }
            }), 409

    reg_user = User(username=username, email=email)
    reg_user.set_password(password=password)

    db.session.add(reg_user)
    db.session.commit()

    return jsonify({
        "username": username,
        "email": email
    }), 201


@app.route("/api/v1/auth/login")
def login():
    data = request.json

    if not data:
        return jsonify({
            "error": {
                "code": "",
                "message": ""
            }
        }), 400

    if "email" not in data or "username" not in data:
        return jsonify({
            "error": {
                "code": "",
                "message": ""
            }
        }), 422

    email = data.get('email')
    password = data.get('password')

    email = email.strip().lower()

    login_user = db.session.execute(
        db.select(User).where(
            (User.email == email)
        )
    ).scalar_one_or_none()

    if login_user is None:
        return jsonify({
            "error": {
                "code": "invalid_email",
                "message": "Invalid email or password!"
            }
        }), 401

    if not login_user.check_password(password):
        return jsonify({
            "error": {
                "code": "invalid_password",
                "message": "Invalid email or password!"
            }
        }), 401

    return jsonify({
        "message": "success!"
    }), 200
