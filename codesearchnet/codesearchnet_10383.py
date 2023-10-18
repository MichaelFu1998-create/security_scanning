def mkdir_p(path):
    """Create a directory *path* with subdirs but do not complain if it exists.

    This is like GNU ``mkdir -p path``.
    """
    try:
        os.makedirs(path)
    except OSError as err:
        if err.errno != errno.EEXIST:
            raise