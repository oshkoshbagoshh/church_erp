"""Main blueprint module."""
from flask import Blueprint, render_template

bp = Blueprint("main", __name__,
               template_folder='templates')

@bp.route("/")
def index():
    """Index page."""
    return render_template("index.html")

@bp.route("/dashboard")
def dashboard():
    """Dashboard page."""
    return render_template("index.html")  # Using index.html as dashboard for now