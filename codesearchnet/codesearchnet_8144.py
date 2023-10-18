def set_log_level(level):
    """
    :param level: the level to set - either a string level name from
                  'frame', 'debug', 'info', 'warning', 'error'
                  or an integer log level from:
                  log.FRAME, log.DEBUG, log.INFO, log.WARNING, log.ERROR
    """
    if isinstance(level, str):
        level = LOG_NAMES[level.lower()]

    logger.setLevel(level)