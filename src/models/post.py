from src.extensions import db


class Post(db.Model):
    __tablename__ = "Post"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="draft")

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    author_id = db.Column(db.Integer, db.ForeignKey('User.id'))
