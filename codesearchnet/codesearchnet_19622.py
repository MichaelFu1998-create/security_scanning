def guess_package_path(searchfrom):
    """
    package path. return None if failed to guess
    """
    from snipy.io import fileutil

    current = searchfrom + '/'
    init_found = False
    pack_found = False
    while not init_found and current != '/':
        current = os.path.dirname(current)
        initfile = os.path.join(current, '__init__.py')
        init_found = os.path.exists(initfile)

    if not init_found:
        # search for breadth
        searchfrom = dirname(searchfrom)

        for folder in fileutil.listfolder(searchfrom):
            current = os.path.join(searchfrom, folder)
            initfile = os.path.join(current, '__init__.py')
            init_found = os.path.exists(initfile)
            if init_found:
                break

    while init_found:
        current = os.path.dirname(current)
        initfile = os.path.join(current, '__init__.py')
        init_found = os.path.exists(initfile)
        pack_found = not init_found

    return current if pack_found else None