import sys
import logging
import logging.handlers


def set_up_logger(debug: bool = True, log_filename: str = None):
    """
    Sets up the logging module.

    :param debug: If True, sets the logging level to DEBUG, otherwise to INFO. Defaults to True.
    :type debug: bool
    :param log_filename: The filename for the log file. If None, logs will only be output to stdout. Defaults to None.
    :type log_filename: str, optional
    :return: None
    """
    level = logging.DEBUG if debug else logging.INFO
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
    )

    logger = logging.getLogger()
    logger.setLevel(level)

    if log_filename:
        handler = logging.FileHandler(filename=log_filename)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logging.debug("Set up logger")
