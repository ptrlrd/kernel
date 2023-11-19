import logging


def setup_logging(level=logging.DEBUG):
    logger = logging.getLogger('nextcord')
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
