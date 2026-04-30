from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

flask_app = Flask(__name__)
flask_app.config.from_object(Config)
db = SQLAlchemy(flask_app)  # for DB connection
migrate = Migrate(flask_app, db)  # for DB structure Migration needs

from app import routes, models  # noqa: E402, F401 # avoid circular imports
