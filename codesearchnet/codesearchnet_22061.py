def _solve_pkg(main_globals):
    '''
    Find parent python path of __main__. From there solve the package
    containing __main__, import it and set __package__ variable.

    :param main_globals: globals dictionary in __main__
    '''
    # find __main__'s file directory and search path
    main_dir, search_path = _try_search_paths(main_globals)
    if not search_path:
        _log_debug('Could not solve parent python path for %r' % main_dir)
        # no candidates for search path, return
        return
    # solve package name from search path
    pkg_str = path.relpath(main_dir, search_path).replace(path.sep, '.')
    # Remove wrong starting string for site-packages
    site_pkgs = 'site-packages.'
    if pkg_str.startswith(site_pkgs):
        pkg_str = pkg_str[len(site_pkgs):]
    assert pkg_str
    _log_debug('pkg_str=%r' % pkg_str)
    # import the package in order to set __package__ value later
    try:
        if '__init__.py' in main_globals['__file__']:
            _log_debug('__init__ script. This module is its own package')
            # The __main__ is __init__.py => its own package
            # If we treat it as a normal module it would be imported twice
            # So we simply reuse it
            sys.modules[pkg_str] = sys.modules['__main__']
            # We need to set __path__ because its needed for
            # relative importing
            sys.modules[pkg_str].__path__ = [main_dir]
            # We need to import parent package, something that would
            # happen automatically in non-faked import
            parent_pkg_str = '.'.join(pkg_str.split('.')[:-1])
            if parent_pkg_str:
                importlib.import_module(parent_pkg_str)
        else:
            _log_debug('Importing package %r' % pkg_str)
            # we need to import the package to be available
            importlib.import_module(pkg_str)
        # finally enable relative import
        main_globals['__package__'] = pkg_str
        return pkg_str
    except ImportError as e:
        # In many situations we won't care if it fails, simply report error
        # main will fail anyway if finds an explicit relative import
        _print_exc(e)