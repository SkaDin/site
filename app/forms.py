from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

from constants import IMAGES


class PostForm(FlaskForm):
    """Форма для создания поста."""
    title = StringField(
        'Введите название тату(17 символов)',
        validators=[DataRequired(message='Поле обязательное!'),
                    Length(1, 17)]
    )
    text = TextAreaField(
        'Всё что хочется рассказать',
        validators=[DataRequired(message='Поле обязательное!'),
                    Length(1, 128)]
    )
    image = FileField(
        'Фото',
        validators=[FileAllowed(
            IMAGES,
            'Только фото!'
        )]
    )
    submit = SubmitField('Отправить')
