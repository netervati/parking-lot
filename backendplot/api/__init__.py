from flask_migrate import Migrate
from flask_cors import CORS
from .routes import db, api
from .config import AppConfig

app = AppConfig()
cors = CORS(app, resources={r'/api/*': {'origins': app.config['ALLOWED_ORIGIN']}})
api.init_app(app)
db.init_app(app)
migrate = Migrate(app, db)
