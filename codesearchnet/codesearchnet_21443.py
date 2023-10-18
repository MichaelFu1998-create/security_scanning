def log_error(error, result):
    """Logs an error
    """
    p = {'error': error, 'result':result}
    _log(TYPE_CODES.ERROR, p)