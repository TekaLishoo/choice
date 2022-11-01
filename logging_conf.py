import logging


def setup_logger(name) -> logging.Logger:
    log_format = "[%(name)s %(module)s:%(lineno)s]\n\t %(message)s \n"
    log_time_format = "%d.%m.%Y %I:%M:%S %p"

    logging.basicConfig(
        format=log_format,
        datefmt=log_time_format,
        level=logging.INFO,
        filename="logging_info.log",
    )

    logger = logging.getLogger(name)
    return logger
