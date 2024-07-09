from flask_migrate import Migrate

from src.app import init_app, db

app = init_app("src.config.DevelopmentConfig")
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run()
