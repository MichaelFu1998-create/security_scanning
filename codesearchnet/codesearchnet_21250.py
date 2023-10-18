def pprint_path(path):
    """
    print information of a pathlib / os.DirEntry() instance with all "is_*" functions.
    """
    print("\n*** %s" % path)
    for attrname in sorted(dir(path)):
        if attrname.startswith("is_"):
            value = getattr(path, attrname)
            print("%20s: %s" % (attrname, value))
    print()