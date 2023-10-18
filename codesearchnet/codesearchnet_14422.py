def _get_module_filename(module):
    """
    Return the filename of `module` if it can be imported.

    If `module` is a package, its directory will be returned.

    If it cannot be imported ``None`` is returned.

    If the ``__file__`` attribute is missing, or the module or package is a
    compiled egg, then an :class:`Unparseable` instance is returned, since the
    source can't be retrieved.

    :param module: A module name, such as ``'test.test_config'``
    :type module: str

    """
    # Split up the module and its containing package, if it has one
    module = module.split('.')
    package = '.'.join(module[:-1])
    module = module[-1]

    try:
        if not package:
            # We aren't accessing a module within a package, but rather a top
            # level package, so it's a straight up import
            module = __import__(module)
        else:
            # Import the package containing our desired module
            package = __import__(package, fromlist=[module])
            # Get the module from that package
            module = getattr(package, module, None)

        filename = getattr(module, '__file__', None)
        if not filename:
            # No filename? Nothing to do here
            return Unparseable()

        # If we get a .pyc, strip the c to get .py so we can parse the source
        if filename.endswith('.pyc'):
            filename = filename[:-1]
            if not os.path.exists(filename) and os.path.isfile(filename):
                # If there's only a .pyc and no .py it's a compile package or
                # egg and we can't get at the source for parsing
                return Unparseable()
        # If we have a package, we want the directory not the init file
        if filename.endswith('__init__.py'):
            filename = filename[:-11]

        # Yey, we found it
        return filename
    except ImportError:
        # Definitely not a valid module or package
        return