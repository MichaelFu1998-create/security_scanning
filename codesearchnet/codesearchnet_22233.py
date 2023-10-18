def mylogger(name=None, filename=None, indent_offset=7, level=_logging.DEBUG, stream_level=_logging.WARN, file_level=_logging.INFO):
    """
    Sets up logging to *filename*.debug.log, *filename*.log, and the terminal. *indent_offset* attempts to line up the lowest indent level to 0. Custom levels:

    * *level*: Parent logging level.
    * *stream_level*: Logging level for console stream.
    * *file_level*: Logging level for general file log.
    """
    if name is not None:
        logger = _logging.getLogger(name)
    else:
        logger = _logging.getLogger()

    logger.setLevel(level)

    fmtr         = IndentFormatter(indent_offset=indent_offset)
    fmtr_msgonly = IndentFormatter('%(funcName)s:%(lineno)d: %(message)s')

    ch = _logging.StreamHandler()
    ch.setLevel(stream_level)
    ch.setFormatter(fmtr_msgonly)
    logger.addHandler(ch)

    if filename is not None:
        debugh = _logging.FileHandler(filename='{}_debug.log'.format(filename), mode='w')
        debugh.setLevel(_logging.DEBUG)
        debugh.setFormatter(fmtr_msgonly)
        logger.addHandler(debugh)

        fh = _logging.FileHandler(filename='{}.log'.format(filename), mode='w')
        fh.setLevel(file_level)
        fh.setFormatter(fmtr)
        logger.addHandler(fh)

    return logger