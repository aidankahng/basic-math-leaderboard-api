from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config


app = Flask(__name__)
cors = CORS(app)

app.config.from_object(Config)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from . import routes, models