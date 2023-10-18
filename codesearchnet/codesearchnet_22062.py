def _log_debug(msg):
    '''
    Log at debug level
    :param msg: message to log
    '''
    if _log_level <= DEBUG:
        if _log_level == TRACE:
            traceback.print_stack()
        _log(msg)