from flask import Flask
from config import BaseConfig


def create_app(config=BaseConfig):
    app = Flask(__name__)
    if config:
        app.config.from_object(config)

    
    # registering app factories
    from models import db
    db.init_app(app)

    from auth import login
    login.init_app(app)

    with app.app_context():
        db.create_all()

    # registering blueprints
    from blueprints.blog import blog
    from blueprints.admin import admin_bp

    app.register_blueprint(blog)
    app.register_blueprint(admin_bp, url_prefix='/'+app.config.get('ADMIN_PORTAL'))

    return app