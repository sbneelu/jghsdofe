from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from jghsdofe.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    app.url_map.strict_slashes = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from jghsdofe.main.routes import main
    from jghsdofe.view.routes import view
    from jghsdofe.edit.routes import edit
    from jghsdofe.users.routes import users
    from jghsdofe.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(view)
    app.register_blueprint(edit)
    app.register_blueprint(users)
    app.register_blueprint(errors)

    return app
