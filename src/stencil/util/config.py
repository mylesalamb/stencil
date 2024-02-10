"""
Utilities to manage the configuration supplied to stencil
"""
import json
import logging
import pathlib
from dataclasses import dataclass
from typing import Any
from typing import Dict

import jsonschema
from stencil.util.exceptions import StencilException

SCHEMA = pathlib.Path(__file__).parent.joinpath("schema.json")
logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class StencilContent:
    """
    Type that represents a stencil content block
    """

    source_directory: pathlib.Path
    output_directory: pathlib.Path
    builder: str


@dataclass(frozen=True)
class StencilBuilder:
    """
    Type that represents a stencil content block
    """

    flavor: str
    config: dict[str, Any]


@dataclass(frozen=True)
class StencilConfig:
    """
    Type that contains a validated stencil config
    """

    content: list[StencilContent]
    builders: dict[str, StencilBuilder]
    variables: dict[str, Any]


def prepare_content(config: list[dict[str, Any]]) -> list[StencilContent]:
    """
    Given raw dictionaries of config types, marshal them to the appropriate type
    """

    def _to_asset(
        source_directory: str, output_directory: str, builder: str
    ) -> StencilContent:
        return StencilContent(
            pathlib.Path(source_directory), pathlib.Path(output_directory), builder
        )

    # Unpacking here is safe through jsonschema validation
    return [_to_asset(**asset) for asset in config]


def parse_and_validate(config: Dict[str, Any]) -> StencilConfig:
    """
    Given a config file as a dictionary, parse and validate the config
    """

    try:
        with open(SCHEMA, "r", encoding="utf-8") as schema:
            jsonschema.validate(config, json.load(schema))
    except jsonschema.exceptions.ValidationError as exc:
        raise StencilException("stencil config malformed") from exc

    content = prepare_content(config["content"])
    builders = {
        name: StencilBuilder(**value) for name, value in config["builders"].items()
    }
    variables = config["variables"]

    validated_config = StencilConfig(content, builders, variables)

    logger.debug("Constructed config: %s", validated_config)

    return validated_config
