def search_file_upwards(name, base=None):
    """ Search for a file named `name` from cwd or given directory to root.
        Return None if nothing's found.
    """
    base = base or os.getcwd()
    while base != os.path.dirname(base):
        if os.path.exists(os.path.join(base, name)):
            return base
        base = os.path.dirname(base)

    return None