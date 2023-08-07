from flask import render_template, helpers, url_for

from admin.models import admin
from app import app


@app.route('/admin')
def index():
    """Отрисовка страницы админки."""
    return render_template(
        'admin/template/admin/index.html',
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=helpers,
        get_url=url_for
    )
