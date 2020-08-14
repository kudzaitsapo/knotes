from flask import Flask
from config import BaseConfig


def create_app(config=BaseConfig):
    app = Flask(__name__)
    if config:
        app.config.from_object(config)

    
    # registering app factories
    from models import db
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # registering blueprints
    from blueprints.blog import blog

    app.register_blueprint(blog)

    return app