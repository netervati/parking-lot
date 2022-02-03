from flask_migrate import Migrate
from .routes import db, api
from .config import AppConfig

app = AppConfig()
db.init_app(app)
api.init_app(app)
Migrate(app, db)
