import os
from flask import Flask

from errors.handlers import register_error_handlers
from routes.auth_routes import auth_bp
from routes.search_routes import search_bp
from routes.spot_routes import spots_bp
from routes.user_routes import users_bp
from db.connection import init_app

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")
app.config["DATABASE"] = os.getenv("DATABASE_PATH", "database.db")

init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(spots_bp)
app.register_blueprint(search_bp)
app.register_blueprint(users_bp)

register_error_handlers(app)

if __name__ == "__main__":
    app.run(debug=True)
