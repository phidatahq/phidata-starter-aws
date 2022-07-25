import logging
import sys


def get_simple_logger(
    logger_name=__name__, logger_level=logging.DEBUG
) -> logging.Logger:

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logger_level)
    simple_formatter = logging.Formatter(
        "%(lineno)d - %(filename)s - %(levelname)s - %(message)s"
    )
    # dttm_formatter = logging.Formatter(
    #     "%(asctime)s - %(lineno)d - %(filename)s - %(levelname)s - %(message)s",
    #     "%Y-%m-%d %H:%M",
    # )
    handler.setFormatter(simple_formatter)

    _logger = logging.getLogger(logger_name)
    _logger.addHandler(handler)
    _logger.setLevel(logger_level)
    _logger.propagate = False
    return _logger


def get_rich_logger(
    logger_name=__name__, logger_level=logging.INFO, show_path=False
) -> logging.Logger:

    from rich.logging import RichHandler

    # https://rich.readthedocs.io/en/latest/reference/logging.html#rich.logging.RichHandler
    # https://rich.readthedocs.io/en/latest/logging.html#handle-exceptions
    rich_handler = RichHandler(
        rich_tracebacks=False, show_time=False, show_path=show_path
    )
    rich_handler.setFormatter(
        logging.Formatter(
            fmt="%(message)s",
            datefmt="[%X]",
        )
    )

    _logger = logging.getLogger(logger_name)
    _logger.addHandler(rich_handler)
    _logger.setLevel(logger_level)
    _logger.propagate = False
    return _logger


logger: logging.Logger = get_rich_logger()
