"""
Tests for the cli frontend to stencil
"""

import functools
import pathlib
from typing import Callable
from typing import Generator
from typing import List
from unittest.mock import Mock
from unittest.mock import patch

import pytest
from click.testing import CliRunner
from click.testing import Result
from stencil.cli import cli

# Mocks inject based on name
# pylint: disable=redefined-outer-name


@pytest.fixture
def runner() -> Callable[[List[str]], Result]:
    """
    Yields an instanstiated click runner
    """
    click_runner = CliRunner()
    return functools.partial(click_runner.invoke, cli)


@pytest.fixture
def mock_serve() -> Generator[Mock, None, None]:
    """
    Mock the underlying call to begin serving content
    """
    mock = patch("stencil.cli.serve_directory")
    yield mock.start()
    mock.stop()


def test_something(runner: Callable[[List[str]], Result], mock_serve: Mock) -> None:
    """
    Test that defaults propagated to impl
    """
    retval = runner(["serve", "--directory", "src"])
    assert retval.exit_code == 0
    mock_serve.assert_called_once_with("localhost", 8080, pathlib.Path("src"))
