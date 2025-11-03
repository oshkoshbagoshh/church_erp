"""Application factory module."""
import os
from pathlib import Path
from flask import Flask
from dotenv import load_dotenv
from .extensions import init_extensions
from .config import config
from .blueprints.main import bp as main_bp
from .blueprints.vendor import bp as vendor_bp

def load_env():
    """Load environment variables from .env file."""
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)

def create_app(config_name=None):
    """Create Flask application."""
    # Load environment variables
    load_env()
    
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")
        if config_name not in config:
            config_name = "development"

    # Initialize app
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')
    
    # Load config
    app.config.from_object(config[config_name])
    
    # Load additional config from environment variables
    app.config.from_prefixed_env(prefix="FLASK")
    
    # Initialize extensions
    init_extensions(app)
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(vendor_bp)
    # Configure logging
    if not app.debug and not app.testing:
        # Add production logging configuration here if needed
        pass
    
    return app