from flask import Flask
from flask_cors import CORS

def create_app(test_config: dict | None = None):
    app = Flask(__name__)

    # Default config
    app.config.update({
        "JSON_SORT_KEYS": False,
        "TESTING": False,
    })

    if test_config:
        app.config.update(test_config)

    CORS(app)

    # Register blueprint
    from .routes import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/")

    return app