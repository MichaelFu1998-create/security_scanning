def amend_filename(filename, amend):
    """Amend a filename with a suffix.

    amend_filename("foo.txt", "_tweak") --> "foo_tweak.txt"

    """
    base, ext = os.path.splitext(filename)
    amended_name = base + amend + ext
    return amended_name