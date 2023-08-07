from flask import url_for, redirect, request, abort
import flask_admin as admin
import flask_login as login
from flask_admin import helpers, Admin
from flask_admin import expose
from flask_admin.contrib import sqla
from werkzeug.security import generate_password_hash

from admin.forms import RegistrationForm, LoginForm
from app import db, app
from app.models import Post
from auth.models import User
from config import Config


class MyModelView(sqla.ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated


class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        if (login.current_user.is_authenticated and
                login.current_user.username == Config.ADMIN_NAME):
            return super(MyAdminIndexView, self).index()
        else:
            return abort(403)

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # Обработка входа в систему.
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)
        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        link = (
            '<p>Don\'t have an account? <a href="' +
            url_for('.register_view') +
            '">Click here to register.</a></p>'
        )
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        form = RegistrationForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = User()
            form.populate_obj(user)
            # Мы хэшируем пароль пользователя,
            # чтобы избежать сохранения его в виде открытого текста в БД.
            user.password = generate_password_hash(form.password.data)
            db.session.add(user)
            db.session.commit()
            login.login_user(user)
            return redirect(url_for('.index'))
        link = (
            '<p>Already have an account? <a href="' +
            url_for('.login_view') +
            '">Click here to log in.</a></p>'
        )
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


admin = Admin(
    app,
    index_view=MyAdminIndexView(),
    base_template='my_master.html',
    template_mode='bootstrap4'
)

admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Post, db.session))
