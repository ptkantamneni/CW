from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from api import app


db = SQLAlchemy()



def init_app(app):
    db.init_app(app)