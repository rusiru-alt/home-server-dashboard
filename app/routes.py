"""Define the dashboard page and API routes."""

from flask import Blueprint, jsonify, render_template

from app import system_info

main = Blueprint("main", __name__)


@main.route("/")
def dashboard():
    """Display the starter dashboard page."""
    return render_template("dashboard.html")


@main.route("/api/status")
def api_status():
    """Return current server status data as JSON."""
    return jsonify(system_info.get_system_status())
