from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.errors import bp as bp_errors
    app.register_blueprint(bp_errors)

    from app.main import bp as bp_main
    app.register_blueprint(bp_main)

    from app.auth import bp as bp_auth
    app.register_blueprint(bp_auth)

    return app


from app import models