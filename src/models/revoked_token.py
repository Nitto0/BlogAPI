from src.extensions import db


class Token(db.Model):
    __tablename__ = "revoked_tokens"

    id = db.Column(db.Integer, primary_key=True)

    jti = db.Column(db.String(64), nullable=False, unique=True)
    token_type = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    revoked_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    expires_at = db.Column(db.DateTime, nullable=False)
