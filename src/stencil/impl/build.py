"""
Utilities for building a stencil project
"""
import logging
import pathlib
from typing import List

from stencil.models import builder
from stencil.models.content import Artefact
from stencil.models.context import BuildContext
from stencil.util.config import StencilConfig
from stencil.util.config import StencilContent


logger = logging.getLogger(__name__)


def enumerate_content(content: StencilContent) -> List[Artefact]:
    """
    Given a config item with source and output directory
    return the artefacts in the directory
    """
    return [
        Artefact(source, content.output_directory / source.name)
        for source in content.source_directory.iterdir()
        if source.is_file()
    ]


def build_from_config(config: StencilConfig, output_directory: pathlib.Path) -> None:
    """
    Given a config file describing a stencil project
    build projects outputs
    """
    ctx = BuildContext(output_directory=output_directory, variables=config.variables)
    builders = {
        name: builder.construct(name, elt) for name, elt in config.builders.items()
    }

    for content_block in config.content:
        for artefact in enumerate_content(content_block):
            builders[content_block.builder].add_content(ctx, artefact)

    logger.debug("Constructed builders: %s", builders)
    logger.debug("Constructed build context: %s", ctx)

    for content_block in config.content:
        for artefact in enumerate_content(content_block):
            logger.debug("Adding %s to builder: %s", artefact, content_block.builder)
            builders[content_block.builder].add_content(ctx, artefact)

    for elt in builders.values():
        elt.build(ctx)
