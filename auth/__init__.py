from flask import Blueprint

bp = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth',
    static_folder='static',  # Пока тест
    template_folder='templates'
)

from auth import routes, models, forms
