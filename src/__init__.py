from flask import Flask

from src.config import Config
from src.extensions import db, migrate, jwt
from src.models import user, post, revoked_token
from src.routes.auth import auth_bp
from src.utils.jwt_callbacks import register_jwt_callbacks


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(auth_bp)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    register_jwt_callbacks()

    return app
