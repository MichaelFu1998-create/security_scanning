def get_app_name():
    """Flask like implementation of getting the applicaiton name via
    the filename of the including file

    """
    fn = getattr(sys.modules['__main__'], '__file__', None)
    if fn is None:
        return '__main__'
    return os.path.splitext(os.path.basename(fn))[0]