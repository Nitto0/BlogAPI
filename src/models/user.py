from werkzeug.security import generate_password_hash, check_password_hash

from src.extensions import db


class User(db.Model):
    __tablename__ = "users"

    __table_args__ = (
        db.CheckConstraint(
            "role IN ('user', 'admin')",
            name="check_user_role"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(80),
        nullable=False,
        unique=True
    )

    email = db.Column(
        db.String(120),
        nullable=False,
        unique=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="user"
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.now()
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.now(),
        onupdate=db.func.now()
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    posts = db.relationship(
        "Post",
        backref="author",
        lazy=True,
        cascade="all, delete-orphan"
    )

    revoked_tokens = db.relationship(
        "RevokedToken",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
