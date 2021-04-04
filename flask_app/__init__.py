from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from config import DevelopmentConfig


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    return app


def init_db(app):
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    return db, migrate


def init_cache(app):
    return FlaskRedis(app)


app = create_app()
db, migrate = init_db(app)
redis = init_cache(app)
marshmallow = Marshmallow(app)

from flask_app import routes
