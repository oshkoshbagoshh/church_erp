#!/usr/bin/env python
"""Main application module."""
import os
from app import create_app
from app.commands import register_commands
from app.extensions import db

app = create_app()
register_commands(app)

@app.shell_context_processor
def make_shell_context():
    """Configure flask shell command to automatically import common objects."""
    return {
        "db": db,
        "app": app,
    }

if __name__ == "__main__":
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    port = int(os.environ.get("FLASK_PORT", 5000))
    app.run(host=host, port=port)

