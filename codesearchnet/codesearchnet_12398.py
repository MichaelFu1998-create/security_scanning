def has_file_with(path, filename, content):
    """
    Check whether *filename* in *path* contains the string *content*.
    """
    try:
        with open(os.path.join(path, filename), "rb") as f:
            return content in f.read()
    except IOError as e:
        if e.errno == errno.ENOENT:
            return False
        else:
            raise