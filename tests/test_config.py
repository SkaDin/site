import os

from dotenv import load_dotenv

from config import Config

load_dotenv()


def test_database():
    assert Config.SQLALCHEMY_DATABASE_URI == os.getenv('SQLALCHEMY_DATABASE_URI'), (
        'Проверьте переменную окружения '
        'SQLALCHEMY_DATABASE_URI в файле .env '
        'она должна быть равна: sqlite:///db.sqlite3'
    )


def test_secret_key():
    assert Config.SECRET_KEY == os.getenv('SECRET_KEY'), (
        'Проверьте переменную окружения '
        'SECRET_KEY в файле .env '
    )
