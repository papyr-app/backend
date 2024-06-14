from flask_migrate import Migrate
from app import init_app, db

app = init_app("config.DevelopmentConfig")
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run()
