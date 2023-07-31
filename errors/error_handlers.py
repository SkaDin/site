from http import HTTPStatus

from flask import render_template

from app import db
from errors import bp


@bp.app_errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error): # noqa
    return render_template('404.html'), HTTPStatus.NOT_FOUND


@bp.app_errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error): # noqa
    db.session.rollback()
    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR
