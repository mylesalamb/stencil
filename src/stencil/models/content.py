"""
Types for managing YASSG content
"""
import pathlib
from dataclasses import dataclass


@dataclass
class Artefact:
    """
    Type that represents a singular item of templated content in YASSG
    """

    source: pathlib.Path
    destination: pathlib.Path

    @property
    def url(self) -> str:
        """
        Returns the url for the artefact in its output directory
        """
        return f"/{'/'.join(self.destination.parts)}"
