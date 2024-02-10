"""
Tests for metadata extraction from content
"""
from stencil.util.metadata import get_embedded_metadata


def test_get_metadata_normal_case() -> None:
    """
    Test normal case where metadata present
    """

    expected_metadata = {"key": 123}
    expected_content = "content"
    string = "\n".join(["---", '{"key": 123}', "---", "content"])

    retval = get_embedded_metadata(string)
    assert retval is not None

    actual_metadata, actual_content = retval
    assert actual_content == expected_content
    assert actual_metadata == expected_metadata


def test_get_no_metadata() -> None:
    """
    Test case where metadata not present
    """

    string = "\n".join(["content"])

    retval = get_embedded_metadata(string)
    assert retval is None


def test_get_no_content() -> None:
    """
    Test case where metadata not present
    """

    expected_metadata = {"key": 123}
    expected_content = ""
    string = "\n".join(["---", '{"key": 123}', "---"])

    retval = get_embedded_metadata(string)
    assert retval is not None

    actual_metadata, actual_content = retval
    assert actual_content == expected_content
    assert actual_metadata == expected_metadata
