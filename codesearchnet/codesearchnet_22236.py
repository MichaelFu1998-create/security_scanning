def false_exit(func):
    """
    If func returns False the program exits immediately.
    """
    @wraps(func)
    def inner(*args, **kwargs):
        ret = func(*args, **kwargs)
        if ret is False:
            if "TMC_TESTING" in os.environ:
                raise TMCExit()
            else:
                sys.exit(-1)
        return ret
    return inner