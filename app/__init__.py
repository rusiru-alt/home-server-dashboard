"""Create and configure the Flask application."""

from flask import Flask


def create_app():
    """Create the Flask app and register its routes."""
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object("app.config.Config")

    from app.routes import main

    app.register_blueprint(main)
    return app
