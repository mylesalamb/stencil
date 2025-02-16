"""
Environment management for the template context
"""

import logging
import pathlib
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Optional

from stencil.models.content import Artefact

logger = logging.getLogger(__name__)


@dataclass
class BuildContext:
    """
    Encapsulates the build environment so that content can reference other content
    """

    output_directory: pathlib.Path
    variables: dict[str, Any]
    content: dict[str, tuple[Artefact, dict[str, Any]]] = field(default_factory=dict)

    def register_content(
        self, name: str, artefact: Artefact, metadata: Optional[dict[str, Any]] = None
    ) -> None:
        """
        Registers content in the build context, so that builders can meaningfully reference
        others content
        """
        logger.debug("Registering identifier: %s, with %s", name, artefact)
        self.content[name] = (artefact, metadata or {})

    def get_artifact_by_name(self, name: str) -> Optional[Artefact]:
        """
        Returns an artifact by its name
        """
        content = self.content.get(name)
        if not content:
            return None

        artefact, _ = content
        return artefact

    def get_artifact_by_metadata(
        self, key: str, value: Any
    ) -> list[tuple[dict[str, Any], Artefact]]:
        """
        Returns artifact by an embedded metadata value
        """

        return [
            (metadata, artefact)
            for artefact, metadata in self.content.values()
            if metadata.get(key) == value
        ]
