from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileSize
from wtforms import (
    BooleanField,
    StringField,
    PasswordField,
    SubmitField,
    FileField,
)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from auth.models import User
from constants import MAX_CONTENT_LENGTH, IMAGES


class LoginForm(FlaskForm):
    username = StringField(
        "Login", validators=[DataRequired(message="Обязательное поле")]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(message="Обязательное поле")]
    )
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("login")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Login", validators=[DataRequired(message="Обязательное поле")]
    )
    email = StringField(
        "email",
        validators=[DataRequired(message="Обязательное поле"), Email()],
    )
    password = PasswordField(
        "Password", validators=[DataRequired(message="Обязательное поле")]
    )
    password2 = PasswordField(
        "Password confirmation",
        validators=[
            DataRequired(message="Обязательное поле"),
            EqualTo("password"),
        ],
    )
    avatar = FileField(
        "Аватар",
        validators=[
            FileAllowed(
                IMAGES,
                message="Только фотографии формата:"
                " jpg, jpe, jpeg, png, gif, svg, bmp",
            ),
            FileSize(MAX_CONTENT_LENGTH),
        ],
    )
    submit = SubmitField("Register")

    def validate_username(self, username):  # noqa
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(f"Этот логин: {user} - уже занят!")

    def validate_email(self, email):  # noqa
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(f"email: {user} - уже занят!")
