from flask_migrate import Migrate

from src.app import init_app, db

app = init_app("src.config.DevelopmentConfig")
migrate = Migrate(app, db)
