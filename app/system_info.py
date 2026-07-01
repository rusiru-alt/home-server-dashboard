"""Collect basic server information for the dashboard."""

import socket
import time

import psutil


UsageStats = dict[str, float | int]
UptimeStats = dict[str, int | str]
SystemStatus = dict[str, str | float | UsageStats | UptimeStats]


def _empty_usage() -> UsageStats:
    """Return a safe empty usage result."""
    return {"percent": 0.0, "used": 0, "total": 0}


def _format_uptime(seconds: int) -> str:
    """Return a readable uptime string from seconds."""
    seconds = max(0, seconds)
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts: list[str] = []
    if days:
        parts.append(f"{days}d")
    if hours or parts:
        parts.append(f"{hours}h")
    if minutes or parts:
        parts.append(f"{minutes}m")
    parts.append(f"{seconds}s")
    return " ".join(parts)


def get_hostname() -> str:
    """Return the server hostname."""
    try:
        return socket.gethostname() or "Unknown"
    except OSError:
        return "Unknown"


def get_local_ip() -> str:
    """Return the server's local IPv4 address."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
    except OSError:
        try:
            return socket.gethostbyname(get_hostname())
        except OSError:
            return "Unknown"


def get_cpu_usage() -> float:
    """Return current CPU usage as a percentage."""
    try:
        return float(psutil.cpu_percent())
    except Exception:
        return 0.0


def get_memory_usage() -> UsageStats:
    """Return RAM usage details."""
    try:
        memory = psutil.virtual_memory()
        return {
            "percent": float(memory.percent),
            "used": int(memory.used),
            "total": int(memory.total),
        }
    except Exception:
        return _empty_usage()


def get_disk_usage() -> UsageStats:
    """Return root filesystem usage details."""
    try:
        disk = psutil.disk_usage("/")
        return {
            "percent": float(disk.percent),
            "used": int(disk.used),
            "total": int(disk.total),
        }
    except Exception:
        return _empty_usage()


def get_uptime() -> UptimeStats:
    """Return uptime in seconds and readable form."""
    try:
        uptime_seconds = max(0, int(time.time() - psutil.boot_time()))
        return {
            "seconds": uptime_seconds,
            "formatted": _format_uptime(uptime_seconds),
        }
    except Exception:
        return {"seconds": 0, "formatted": "Unknown"}


def get_system_status() -> SystemStatus:
    """Return all dashboard metrics in one dictionary."""
    return {
        "hostname": get_hostname(),
        "local_ip": get_local_ip(),
        "cpu_usage": get_cpu_usage(),
        "memory_usage": get_memory_usage(),
        "disk_usage": get_disk_usage(),
        "uptime": get_uptime(),
    }


def get_ip_address() -> str:
    """Return the local IPv4 address for older callers."""
    return get_local_ip()


def get_ram_usage() -> UsageStats:
    """Return RAM usage details for older callers."""
    return get_memory_usage()
