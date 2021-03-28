from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from config import ProductionConfig, DevelopmentConfig


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    return app


app = create_app()
db = SQLAlchemy(app)
redis = FlaskRedis(app)

with app.app_context():
    from flask_app import routes
    from flask_app import models

    db.create_all()
