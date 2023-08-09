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


def test_people_folder():
    people_folder_config = os.path.join('app/static', 'people_photo')
    people_folder_actual = os.path.abspath(Config.PEOPLE_FOLDER)
    assert os.path.samefile(people_folder_config, people_folder_actual), (
        'Проверьте директорию people_photo, '
        'она должна быть одинаковой в конфигурации и по факту'
    )
