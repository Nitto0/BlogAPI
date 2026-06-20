from flask import Flask
from flask_migrate import Migrate

from src.config import Config
from src.extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)

    return app
