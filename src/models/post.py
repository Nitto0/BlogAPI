from src.extensions import db


class Post(db.Model):
    __tablename__ = "posts"

    __table_args__ = (
        db.CheckConstraint(
            "status IN ('draft', 'published')",
            name="check_post_status"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    content = db.Column(db.Text, nullable=False)

    status = db.Column(db.String(20), nullable=False, default="draft")

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

    published_at = db.Column(db.DateTime, nullable=True)

    author_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
