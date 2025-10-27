import os
from flask import Flask, render_template
from .db import init_app
from .auth import bp as auth_bp
from .game import bp as game_bp
from .scores import bp as scores_bp

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "zahlenspiel.db"),
        PASSWORD_METHOD="pbkdf2:sha256",
        PASSWORD_SALT_LENGTH=16,
        PASSWORD_MIN_LENGTH=8,
        LOGIN_REQUIRED_FLASH=True,
    )

    if test_config is not None:
        app.config.update(test_config)

    # Instance-Ordner sicherstellen
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # DB & Blueprints
    init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(game_bp)
    app.register_blueprint(scores_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
