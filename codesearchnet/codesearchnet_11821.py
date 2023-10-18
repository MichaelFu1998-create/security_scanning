def set_cwd(new_path):
    """
    Usage:

        with set_cwd('/some/dir'):
            walk_around_the_filesystem()
    """
    try:
        curdir = os.getcwd()
    except OSError:
        curdir = new_path
    try:
        os.chdir(new_path)
        yield
    finally:
        os.chdir(curdir)