# Home Server Monitoring Dashboard

A lightweight Flask web dashboard for viewing basic information about a Debian 13
home server. This project is intended as a beginner-friendly way to learn web
development, Linux deployment, and local networking.

## Planned Features

- Display the server hostname and local IP address
- Show CPU and RAM usage
- Show disk usage
- Show server uptime
- Report the status of selected services
- Refresh dashboard data without reloading the page

## Technology Stack

- Python
- Flask
- psutil
- HTML, CSS, and JavaScript
- Debian 13 for the planned deployment environment

## Security Note

This dashboard is intended for LAN-only use. Do not expose the Flask development
server directly to the public internet. A future deployment should use a
production WSGI server, a reverse proxy, firewall rules, and authentication where
appropriate.

## Getting Started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

On Windows PowerShell, activate the virtual environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then open `http://127.0.0.1:5000` in a browser.

## Project Status

This repository currently contains the initial project structure and starter
code. Monitoring features will be implemented in later stages.
