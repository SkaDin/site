from flask import Blueprint

bp = Blueprint(
    'errors',
    __name__
)

from errors import error_handlers # noqa