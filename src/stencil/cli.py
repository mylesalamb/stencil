"""
stencil CLI / exposed entrypoints
"""
import io
import json
import logging
import pathlib

import click
from stencil.impl.build import build_from_config
from stencil.impl.serve import serve_directory
from stencil.util.config import parse_and_validate
from stencil.util.config import StencilConfig
from stencil.util.logging import configure_logging

logger = logging.getLogger(__name__)


def _get_config(
    ctx: click.Context, param: click.Option, value: io.TextIOWrapper
) -> StencilConfig:
    """
    Helper to take a file object and yield a stencil config
    """
    del ctx, param

    return parse_and_validate(json.load(value))


@click.group()
@click.option(
    "--verbose", "-v", is_flag=True, default=False, help="Enable verbose log output"
)
def cli(verbose: bool) -> None:
    """
    stencil is a simple static site generator written in python
    that processes HTML templates and content, written in either
    markdown or HTML to facilitate painless development of websites
    """
    configure_logging(verbose)


@cli.group()
def build() -> None:
    """
    Subcommands that manages building stencil content
    """


@build.command("project")
@click.option(
    "--config",
    "-c",
    type=click.File(mode="r", encoding="utf-8"),
    required=True,
    callback=_get_config,
    help="Location of stencil config file, or '-' to indicate that the config "
    "should be read from stdin",
)
@click.option(
    "--output-directory",
    "-o",
    type=click.Path(
        exists=False,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        path_type=pathlib.Path,
    ),
    required=True,
    help="Location for the build outputs of stencil",
)
def build_project(config: StencilConfig, output_directory: pathlib.Path) -> None:
    """
    Builds a stencil project
    """
    build_from_config(config, output_directory)


@cli.command()
@click.option(
    "--host", default="localhost", help="Host to bind to, to serve content from"
)
@click.option(
    "--port", default=8080, type=int, help="Port to bind to, to serve content from"
)
@click.option(
    "--directory",
    type=pathlib.Path,
    required=True,
    help="Directory to serve content from",
)
def serve(host: str, port: int, directory: pathlib.Path) -> None:
    """
    Serves a stencil project
    """
    serve_directory(
        host,
        port,
        directory,
    )
