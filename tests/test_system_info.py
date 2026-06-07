"""Placeholder tests for the system information helpers."""

from app import system_info


def test_hostname_placeholder():
    """The hostname helper should currently return placeholder text."""
    assert system_info.get_hostname() == "Not implemented"


def test_cpu_usage_placeholder():
    """The CPU helper should currently return no measurement."""
    assert system_info.get_cpu_usage() is None
