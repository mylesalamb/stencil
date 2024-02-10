"""
Logging configuration for YASSG
"""
import logging.config


def configure_logging(verbose: bool) -> None:
    """
    Configures the logging output to a nice format
    """

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {"format": "%(asctime)s [%(levelname)s]: %(message)s"},
        },
        "handlers": {
            "default": {
                "level": "WARNING" if not verbose else "DEBUG",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",  # Default is stderr
            },
        },
        "loggers": {
            "": {  # root logger
                "handlers": ["default"],
                "level": "WARNING" if not verbose else "DEBUG",
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(config)
