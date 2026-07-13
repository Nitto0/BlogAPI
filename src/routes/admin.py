from flask import Blueprint

admin_bd = Blueprint(
    "admin",
    __name__,
    url_prefix="/api/v1/admin"
)
