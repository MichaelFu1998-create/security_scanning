def fail(value, context_info=None, src_exception=None, err_condition=None):
    """Wrapper to raise (and log) DAVError."""
    if isinstance(value, Exception):
        e = as_DAVError(value)
    else:
        e = DAVError(value, context_info, src_exception, err_condition)
    _logger.error("Raising DAVError {}".format(e.get_user_info()))
    raise e