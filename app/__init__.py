from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config


app = Flask(__name__)  # instance_relative_config=True) для разработки
app.config.from_object(Config)
# app.config.from_pyfile('config.py') для разработки
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'auth.login'
login.login_message = 'Зарегистрируйтесь для доступа к странице!'
bootstrap = Bootstrap(app)


from errors import bp as errors_bp

app.register_blueprint(errors_bp)

from auth import bp as auth_bp

from admin import bp as admin_bp

app.register_blueprint(admin_bp)

app.register_blueprint(auth_bp)

from app import routes
