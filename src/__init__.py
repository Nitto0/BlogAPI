from flask import Flask

from src.config import Config
from src.extensions import db, migrate, jwt
from src.models import user, post


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    return app
