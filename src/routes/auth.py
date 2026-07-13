from flask import request, jsonify
from pydantic import ValidationError
from flask import Blueprint
from flask import current_app
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from sqlalchemy.exc import SQLAlchemyError

from src.schemas.user import UserSchema
from src.models.user import User
from src.extensions import db

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/v1/auth"
)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)

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
        }), 422

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    try:
        validate_reg = UserSchema(username=username, password=password, email=email)
    except ValidationError:
        return jsonify({
            "error": {
                "code": "validation_error",
                "message": "Invalid data!"
            }
        }), 422

    email = str(validate_reg.email).strip().lower()
    username = validate_reg.username.strip().lower()
    password = str(validate_reg.password)

    try:
        existing_user = db.session.execute(
            db.select(User).where(
                (User.email == email) | (User.username == username)
            )
        ).scalar_one_or_none()
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception(
            "Database error during checking"
        )

        return jsonify({
            "error": {
                "code": "internal_error",
                "message": "Internal server error"
            }
        }), 500

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

    try:
        db.session.add(reg_user)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception(
            "Database error during registration"
        )

        return jsonify({
            "error": {
                "code": "internal_error",
                "message": "Internal server error"
            }
        }), 500

    return jsonify({
        "username": username,
        "email": email
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": {
                "code": "invalid_json",
                "message": "Incorrect data"
            }
        }), 400

    if "email" not in data or "password" not in data:
        return jsonify({
            "error": {
                "code": "validation_error",
                "message": "Email and password are required"
            }
        }), 422

    email = data.get('email')
    password = data.get('password')

    email = email.strip().lower()

    try:
        login_user = db.session.execute(
            db.select(User).where(User.email == email)
        ).scalar_one_or_none()
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception(
            "Database error during login"
        )

        return jsonify({
            "error": {
                "code": "internal_error",
                "message": "Internal server error"
            }
        }), 500

    if login_user is None or not login_user.check_password(password):
        return jsonify({
            "error": {
                "code": "invalid_credentials",
                "message": "Invalid email or password!"
            }
        }), 401

    if not login_user.is_active:
        return jsonify({
            "error": {
                "code": "account_inactive",
                "message": "Account is blocked!"
            }
        }), 403

    access_token = create_access_token(
        identity=str(login_user.id)
    )

    refresh_token = create_refresh_token(
        identity=str(login_user.id)
    )

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": login_user.id,
            "username": login_user.username,
            "email": login_user.email
        }
    }), 200
