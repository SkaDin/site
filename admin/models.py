from flask_admin.contrib.sqla import ModelView

from app import db
from app import admin
from auth.models import User
from app.models import Post


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
