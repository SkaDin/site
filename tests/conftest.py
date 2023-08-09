import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv
from mixer.backend.flask import mixer as _mixer

load_dotenv()

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR))


try:
    from app import app, db
    from app.models import Post

except NameError:
    raise AssertionError(
        'Не обнаружен объект приложения. Создайте экземпляр класса Flask и назовите его app.',
    )
except ImportError as exc:
    if any(obj in exc.name for obj in ['models', 'Post']):
        raise AssertionError('В файле models не найдена модель Post')
    raise AssertionError(
        'Не обнаружен объект класса SQLAlchemy. Создайте его и назовите db.'
    )


@pytest.fixture
def test_config(tmp_path):
    tmp_path = Path(__file__).resolve().parent.parent
    return tmp_path


@pytest.fixture
def default_app():
    with app.app_context():
        yield app


@pytest.fixture
def _app(tmp_path): # noqa
    db_path = tmp_path / 'test_db.sqlite3'
    db_uri = 'sqlite:///' + str(db_path)
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': db_uri,
        'WTF_CSRF_ENABLED': False,
    })
    with app.app_context():
        db.create_all()
    yield app
    db.drop_all()
    db.session.close()
    db_path.unlink()


@pytest.fixture
def client(_app):
    return _app.test_client()


@pytest.fixture
def cli_runner():
    return app.test_cli_runner()


@pytest.fixture
def mixer():
    _mixer.init_app(app)
    return _mixer


@pytest.fixture
def short_python_url(mixer):
    return mixer.blend(Post, original='https://www.python.org', short='py')
