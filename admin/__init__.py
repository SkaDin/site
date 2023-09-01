from flask import Blueprint


bp = Blueprint(
    "admin_page",
    __name__,
    url_prefix="/admin",
    static_folder="static",
    template_folder="templates",
)


from admin import routes, models, forms
