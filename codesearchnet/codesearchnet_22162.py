def error(code: int, *args, **kwargs) -> HedgehogCommandError:
    """
    Creates an error from the given code, and args and kwargs.

    :param code: The acknowledgement code
    :param args: Exception args
    :param kwargs: Exception kwargs
    :return: the error for the given acknowledgement code
    """
    # TODO add proper error code
    if code == FAILED_COMMAND and len(args) >= 1 and args[0] == "Emergency Shutdown activated":
        return EmergencyShutdown(*args, **kwargs)
    return _errors[code](*args, **kwargs)