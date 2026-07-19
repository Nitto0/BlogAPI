from sqlalchemy.exc import SQLAlchemyError
from flask import (
    Blueprint,
    jsonify,
    current_app,
)
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

from src.extensions import db
from src.models.user import User


admin_bd = Blueprint(
    "users",
    __name__,
    url_prefix="/api/v1/users"
)


@admin_bd.route("/me", methods=['GET'])
@jwt_required()
def me_profile():
    current_user_id = int(get_jwt_identity())
    token_data = get_jwt()

    if current_user_id is None:
        return jsonify({
            "error": {
                "code": "",
                "message": ""
            }
        }), 401

    if token_data['type'] == 'refresh':
        return jsonify({
            "error": {
                "code": "",
                "message": ""
            }
        }), 401

    try:
        user = db.session.execute(
            db.select(User).where(User.id == current_user_id)
        ).scalar_one_or_none()
    except SQLAlchemyError:
        db.session.rollback()

        current_app.logger.exception(
            "Database error during logout"
        )

        return jsonify({
            "error": {
                "code": "internal_error",
                "message": "Internal server error"
            }
        }), 500

    if user is None:
        return jsonify({
            "error": {
                "code": "user_not_found",
                "message": "User not found"
            }
        }), 404

    if not user.is_active:
        return jsonify({
            "error": {
                "code": "account_inactive",
                "message": "Account is blocked"
            }
        }), 403

    return jsonify({
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        }
    }), 200
