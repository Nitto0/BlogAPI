from flask import jsonify

from src.extensions import db, jwt
from src.models.revoked_token import RevokedToken


def register_jwt_callbacks():

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]

        revoked_token = db.session.execute(
            db.select(RevokedToken).where(RevokedToken.jti == jti)
        ).scalar_one_or_none()

        return revoked_token is not None

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "error": {
                "code": "token_revoked",
                "message": "Token has been revoked"
            }
        }), 401
