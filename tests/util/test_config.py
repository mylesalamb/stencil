"""
Tests for config parsing in stencil
"""
from typing import Any

from stencil.util.config import parse_and_validate


def test_valid_config() -> None:
    """
    Test that when the config has required fields
    that the parse function does not throw
    """

    config: dict[str, Any] = {
        "content": {"templates": [], "assets": [], "static": []},
        "variables": {},
    }
    parse_and_validate(config)


def test_vars_optional() -> None:
    """
    Test that when the config is missing optional fields
    that the parse function does not throw
    """
    config: dict[str, Any] = {"content": {"templates": [], "assets": [], "static": []}}
    parse_and_validate(config)
