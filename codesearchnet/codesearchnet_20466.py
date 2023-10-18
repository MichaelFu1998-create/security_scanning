def error_handler(func):
    """Decorator to error handling."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Run actual function and if exception catched and error handler enabled
        put traceback to log file
        """
        try:
            return func(*args, **kwargs)
        except BaseException as err:
            # Do not catch exceptions on testing
            if BOOTSTRAPPER_TEST_KEY in os.environ:
                raise
            # Fail silently if error handling disabled
            if ERROR_HANDLER_DISABLED:
                return True
            # Otherwise save traceback to log
            return save_traceback(err)
    return wrapper