"""Tests for the system information helpers."""

import unittest
from types import SimpleNamespace
from unittest.mock import patch

from app import system_info


class SystemInfoTests(unittest.TestCase):
    """Verify metric collection and safe fallbacks."""

    def test_get_hostname_returns_socket_hostname(self) -> None:
        """Hostname should come from the socket module."""
        with patch("app.system_info.socket.gethostname", return_value="home-server"):
            self.assertEqual(system_info.get_hostname(), "home-server")

    def test_get_hostname_falls_back_to_unknown(self) -> None:
        """Hostname should not raise if socket lookup fails."""
        with patch("app.system_info.socket.gethostname", side_effect=OSError):
            self.assertEqual(system_info.get_hostname(), "Unknown")

    def test_get_local_ip_returns_socket_address(self) -> None:
        """Local IP should come from the active IPv4 socket."""
        with patch("app.system_info.socket.socket") as socket_factory:
            sock = socket_factory.return_value.__enter__.return_value
            sock.getsockname.return_value = ("192.168.1.25", 54321)

            self.assertEqual(system_info.get_local_ip(), "192.168.1.25")
            sock.connect.assert_called_once_with(("8.8.8.8", 80))

    def test_get_cpu_usage_returns_percentage(self) -> None:
        """CPU usage should return a numeric percentage."""
        with patch("app.system_info.psutil.cpu_percent", return_value=12.5):
            self.assertEqual(system_info.get_cpu_usage(), 12.5)

    def test_get_cpu_usage_falls_back_to_zero(self) -> None:
        """CPU usage should not raise if psutil fails."""
        with patch("app.system_info.psutil.cpu_percent", side_effect=RuntimeError):
            self.assertEqual(system_info.get_cpu_usage(), 0.0)

    def test_get_memory_usage_returns_expected_fields(self) -> None:
        """Memory usage should include percent, used, and total."""
        memory = SimpleNamespace(percent=33.3, used=1000, total=3000)

        with patch("app.system_info.psutil.virtual_memory", return_value=memory):
            self.assertEqual(
                system_info.get_memory_usage(),
                {"percent": 33.3, "used": 1000, "total": 3000},
            )

    def test_get_disk_usage_returns_expected_fields(self) -> None:
        """Disk usage should include percent, used, and total."""
        disk = SimpleNamespace(percent=44.4, used=2000, total=5000)

        with patch("app.system_info.psutil.disk_usage", return_value=disk):
            self.assertEqual(
                system_info.get_disk_usage(),
                {"percent": 44.4, "used": 2000, "total": 5000},
            )

    def test_get_uptime_returns_seconds_and_formatted_value(self) -> None:
        """Uptime should include raw seconds and readable text."""
        with (
            patch("app.system_info.time.time", return_value=1000),
            patch("app.system_info.psutil.boot_time", return_value=700),
        ):
            self.assertEqual(
                system_info.get_uptime(),
                {"seconds": 300, "formatted": "5m 0s"},
            )

    def test_get_system_status_combines_metrics(self) -> None:
        """System status should collect all dashboard metrics."""
        with (
            patch("app.system_info.get_hostname", return_value="home-server"),
            patch("app.system_info.get_local_ip", return_value="192.168.1.25"),
            patch("app.system_info.get_cpu_usage", return_value=12.5),
            patch(
                "app.system_info.get_memory_usage",
                return_value={"percent": 33.3, "used": 1000, "total": 3000},
            ),
            patch(
                "app.system_info.get_disk_usage",
                return_value={"percent": 44.4, "used": 2000, "total": 5000},
            ),
            patch(
                "app.system_info.get_uptime",
                return_value={"seconds": 300, "formatted": "5m 0s"},
            ),
        ):
            self.assertEqual(
                system_info.get_system_status(),
                {
                    "hostname": "home-server",
                    "local_ip": "192.168.1.25",
                    "cpu_usage": 12.5,
                    "memory_usage": {"percent": 33.3, "used": 1000, "total": 3000},
                    "disk_usage": {"percent": 44.4, "used": 2000, "total": 5000},
                    "uptime": {"seconds": 300, "formatted": "5m 0s"},
                },
            )


if __name__ == "__main__":
    unittest.main()
