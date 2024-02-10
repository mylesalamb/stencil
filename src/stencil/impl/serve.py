"""
Utilities for serving build website content
"""
import http.server
import logging
import os
import pathlib
import socketserver

logger = logging.getLogger(__name__)


def serve_directory(hostname: str, port: int, directory: pathlib.Path) -> None:
    """
    Serves file content from @directory on @hostname:@port
    """
    os.chdir(directory)
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer((hostname, port), handler)
    try:
        logger.info("Serving on http://%s:%s", hostname, port)
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.warning("Caught keyboard interrupt")
