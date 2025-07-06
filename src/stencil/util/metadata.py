"""
Utilities for extracting json metadata headers in files
"""

import json
import logging
import pathlib
import re
from typing import Any
from typing import Optional

_METADATA_WRAPPER = r"(?:---)"
METADATA_REGEX = f"^{_METADATA_WRAPPER}\n(.+?){_METADATA_WRAPPER}(?:\n)?(.*)$"
REGEX = re.compile(METADATA_REGEX, re.S | re.M)

logger = logging.getLogger(__name__)


def get_embedded_metadata(string: str) -> Optional[tuple[dict[str, Any], str]]:
    """
    Returns embedded json documents from files
    """
    result = REGEX.search(string)

    if not result:
        return None
    try:
        return json.loads(result.group(1)), result.group(2)
    except json.decoder.JSONDecodeError:
        logger.fatal("Could not extract metadata from header: %s", result.group(1))
        raise


def get_file_content(path: pathlib.Path) -> tuple[dict[str, Any], str]:
    """
    Returns the metadata associated with content and the content of the file
    """

    with open(path, encoding="utf-8") as f:
        raw_content = f.read()

    if content_tuple := get_embedded_metadata(raw_content):
        return content_tuple

    return {}, raw_content
