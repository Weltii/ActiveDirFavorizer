import logging


def init_logging():
    log = logging.getLogger()
    log.setLevel(logging.INFO)

    formatter = logging.Formatter("%(levelname)s %(asctime)s - %(message)s")

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    log.addHandler(ch)
