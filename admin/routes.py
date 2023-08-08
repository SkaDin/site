from flask import render_template, helpers, url_for, abort
from flask_login import current_user

from admin.models import admin
from app import app
from constants import FORBIDDEN


@app.route('/admin')
def index():
    """Отрисовка страницы админки."""
    return render_template(
        'indexx.html',
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=helpers,
        get_url=url_for
    )
