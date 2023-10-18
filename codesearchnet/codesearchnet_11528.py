def retries(max_tries, exceptions=(Exception,)):
    """Function decorator implementing retrying logic.

    exceptions: A tuple of exception classes; default (Exception,)

    The decorator will call the function up to max_tries times if it raises
    an exception.

    By default it catches instances of the Exception class and subclasses.
    This will recover after all but the most fatal errors. You may specify a
    custom tuple of exception classes with the 'exceptions' argument; the
    function will only be retried if it raises one of the specified
    exceptions.
    """
    def decorator(func):
        def function(*args, **kwargs):

            retries_left = max_tries
            while retries_left > 0:
                try:
                    retries_left -= 1
                    return func(*args, **kwargs)

                except exceptions as exc:
                    # Don't retry for PandoraExceptions - unlikely that result
                    # will change for same set of input parameters.
                    if isinstance(exc, PandoraException):
                        raise
                    if retries_left > 0:
                        time.sleep(delay_exponential(
                            0.5, 2, max_tries - retries_left))
                    else:
                        raise

        return function

    return decorator