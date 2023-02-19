import logging

log_format = "%(asctime)s [%(levelname)s] - %(name)s - %(funcName)s: %(message)s"

file_handler = logging.FileHandler("application.logs")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(log_format))


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    return logger


logger = get_logger(__name__)
