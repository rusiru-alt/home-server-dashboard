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
    """Return placeholder server status data as JSON."""
    return jsonify(
        hostname=system_info.get_hostname(),
        ip_address=system_info.get_ip_address(),
        cpu_usage=system_info.get_cpu_usage(),
        ram_usage=system_info.get_ram_usage(),
        disk_usage=system_info.get_disk_usage(),
        uptime=system_info.get_uptime(),
    )
