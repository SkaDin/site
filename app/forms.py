from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed

from app.constants import IMAGES


class PostForm(FlaskForm):
    """Форма для создания поста."""
    title = StringField(
        'Введите название тату',
        validators=[DataRequired(message='Поле обязательное!'),
                    Length(1, 124)]
    )
    text = TextAreaField(
        'Всё что хочется рассказать',
        validators=[DataRequired(message='Поле обязательное!')]
    )
    image = FileField(
        'Фото',
        validators=[FileAllowed(
            IMAGES,
            'Только фото!'
        )]
    )
    submit = SubmitField('Отправить')
