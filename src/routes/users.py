from flask import Blueprint

admin_bd = Blueprint(
    "users",
    __name__,
    url_prefix="/api/v1/users"
)
