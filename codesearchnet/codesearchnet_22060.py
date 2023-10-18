def _try_search_paths(main_globals):
    '''
    Try different strategies to found the path containing the __main__'s file.
    Will try strategies, in the following order:
        1. Building file's path with PWD env var.
        2. Building file's path from absolute file's path.
        3. Buidling file's path from real file's path.

    :param main_globals: globals dictionary in __main__
    '''
    # try with abspath
    fl = main_globals['__file__']
    search_path = None
    if not path.isabs(fl) and os.getenv('PWD'):
        # Build absolute path from PWD if possible
        cwd_fl = path.abspath(path.join(os.getenv('PWD'), fl))
        main_dir = path.dirname(cwd_fl)
        search_path = _get_search_path(main_dir, sys.path)

    if not search_path:
        # try absolute strategy (will fail on some symlinks configs)
        main_dir = path.dirname(path.abspath(fl))
        search_path = _get_search_path(main_dir, sys.path)

    if not search_path:
        # try real path strategy
        main_dir = path.dirname(path.realpath(fl))
        sys_path = [path.realpath(p) for p in sys.path]
        search_path = _get_search_path(main_dir, sys_path)

    return main_dir, search_path