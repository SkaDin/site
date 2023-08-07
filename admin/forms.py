import flask_login as login
from werkzeug.security import check_password_hash

from wtforms import Form, StringField, PasswordField
from wtforms.validators import InputRequired, ValidationError

from app import app, db
from auth.models import User
from constants import NULL


class LoginForm(Form):
    login = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])

    def validate_login(self, field): # noqa
        user = self.get_user()
        if user is None:
            raise ValidationError('Invalid user.')
        if not check_password_hash(user.password, self.password.data):
            raise ValidationError('Invalid password')

    def get_user(self):
        return db.sessiom.query(User).filter_by(login=self.login.data).first()


class RegistrationForm(Form):
    login = StringField(validators=[InputRequired()])
    email = StringField()
    password = PasswordField(validators=[InputRequired()])

    def validate_login(self, field): # noqa
        if db.session.query(User).filter_by(
                login=self.login.data
        ).count() > NULL:
            raise ValidationError('Duplicate username')


def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Создаём пользовательскую функцию загрузки
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)
