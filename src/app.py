from flask import Flask
from config import Config
from models.database import db
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)


@app.before_request
def create_table():
    db.create_all()
