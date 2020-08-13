from flask import Flask
from config import BaseConfig


def create_app(config=BaseConfig):
    app = Flask(__name__)
    if config:
        app.config.from_object(config)

    # registering blueprints
    from blueprints.blog import blog

    app.register_blueprint(blog)

    return app