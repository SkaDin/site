from sqlalchemy import inspect

from app.models import Post
from auth.models import User


def check_model_fields(model, required_fields):
    """Общая логика проверки полей модели."""
    inspector = inspect(model)
    fields = [column.name for column in inspector.columns]
    print(fields)
    assert all(field in fields for field in required_fields), (
        f'В модели не найдены все необходимые поля. '
        f'Проверьте модель: в ней должны быть поля {", ".join(required_fields)}.'
    )


class TestModel:
    """Тестирование моделей."""

    def test_user_model_fields(self):
        required_fields = ['id', 'username', 'email', 'password', 'avatar']
        check_model_fields(User, required_fields)

    def test_post_model_fields(self):
        required_fields = ['id', 'title', 'image', 'text', 'timestamp', 'user_id']
        check_model_fields(Post, required_fields)
