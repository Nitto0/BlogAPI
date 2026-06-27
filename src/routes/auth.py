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

    reg_user = User(username=username, email=email)
    reg_user.set_password(password=password)

    db.session.add(reg_user)
    db.session.commit()

    return jsonify({
        "username": username,
        "email": email
    }), 201
