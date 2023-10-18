def find_package_path(searchfrom):
    """
    package path. return None if failed to guess
    """

    current = searchfrom + '/'
    init_found = False
    pack_found = False
    while not init_found and current != '/':
        current = os.path.dirname(current)
        initfile = os.path.join(current, '__init__.py')
        init_found = os.path.exists(initfile)

    while init_found:
        current = os.path.dirname(current)
        initfile = os.path.join(current, '__init__.py')
        init_found = os.path.exists(initfile)
        pack_found = not init_found

    return current if pack_found else None