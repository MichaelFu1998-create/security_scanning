def src_to_html(fpath):
    """
    Returns content of the given 'fpath' with HTML annotations for syntax
    highlighting
    """

    if not os.path.exists(fpath):
        return "COULD-NOT-FIND-TESTCASE-SRC-AT-FPATH:%r" % fpath

    # NOTE: Do SYNTAX highlight?

    return open(fpath, "r").read()