def atomic_write(filename):
    """
    Open a NamedTemoraryFile handle in a context manager
    """
    f = _tempfile(os.fsencode(filename))

    try:
        yield f

    finally:
        f.close()
        # replace the original file with the new temp file (atomic on success)
        os.replace(f.name, filename)