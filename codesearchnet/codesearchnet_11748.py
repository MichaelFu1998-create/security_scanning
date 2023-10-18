def package_version(name, python_cmd='python'):
    """
    Get the installed version of a package

    Returns ``None`` if it can't be found.
    """
    cmd = '''%(python_cmd)s -c \
        "import pkg_resources;\
        dist = pkg_resources.get_distribution('%(name)s');\
        print dist.version"
        ''' % locals()
    res = run(cmd, quiet=True)
    if res.succeeded:
        return res
    return