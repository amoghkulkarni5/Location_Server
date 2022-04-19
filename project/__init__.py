from flask import Flask
import os


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-lol'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    os.environ['PYTHONPATH'] = os.getcwd()

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
