def create_logger(name,
                  filename=None,
                  logging_level=logging.DEBUG):
    """Create a logger object."""
    logger = logging.getLogger(name)
    formatter = logging.Formatter(('%(asctime)s - %(name)s - '
                                   '%(levelname)-8s - %(message)s'))

    if filename:
        fh = logging.FileHandler(filename=filename)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.setLevel(logging_level)

    return logger