def set_debug():
    """ activates error messages, useful during development """
    logging.basicConfig(level=logging.WARNING)
    peony.logger.setLevel(logging.DEBUG)