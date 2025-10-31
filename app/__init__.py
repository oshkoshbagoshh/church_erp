"""
Flask application for Church ERP
"""
from flask import Flask
from app.config import Config
from app.extensions import db, migrate


def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')

    app.config.from_object(config_class)

    # Initialize extensions
