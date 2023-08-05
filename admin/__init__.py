from flask_admin.contrib.sqla import ModelView
from app import app, db

from app.models import Post
from auth.models import User
from app import Admin


admin = Admin(app, name='myblog', template_mode='bootstrap3')

admin.add_views(ModelView(User, db.session))
admin.add_views(ModelView(Post, db.session))
