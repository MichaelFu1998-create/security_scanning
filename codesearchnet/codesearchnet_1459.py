def __getLogger(cls):
    """ Get the logger for this object.

    :returns: (Logger) A Logger object.
    """
    if cls.__logger is None:
      cls.__logger = opf_utils.initLogger(cls)
    return cls.__logger