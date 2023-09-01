from http import HTTPStatus

from flask import render_template

from app import db
from constants import NOT_FOUND, INTERNAL_SERVER_ERROR, FORBIDDEN
from errors import bp


@bp.app_errorhandler(NOT_FOUND)
def page_not_found(error):  # noqa
    return render_template("404.html"), HTTPStatus.NOT_FOUND


@bp.app_errorhandler(INTERNAL_SERVER_ERROR)
def internal_error(error):  # noqa
    db.session.rollback()
    return render_template("500.html"), HTTPStatus.INTERNAL_SERVER_ERROR


@bp.app_errorhandler(FORBIDDEN)
def forbidden_error(error):  # noqa
    return render_template("403.html"), HTTPStatus.FORBIDDEN
