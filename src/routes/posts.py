from flask import Blueprint

admin_bd = Blueprint(
    "posts",
    __name__,
    url_prefix="/api/v1/posts"
)
