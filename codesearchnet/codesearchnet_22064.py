def _init(frame, log_level=ERROR):
    '''
    Enables explicit relative import in sub-modules when ran as __main__
    :param log_level: module's inner logger level (equivalent to logging pkg)
    '''
    global _log_level
    _log_level = log_level
    # now we have access to the module globals
    main_globals = frame.f_globals

    # If __package__ set or it isn't the __main__, stop and return.
    # (in some cases relative_import could be called once from outside
    # __main__ if it was not called in __main__)
    # (also a reload of relative_import could trigger this function)
    pkg = main_globals.get('__package__')
    file_ = main_globals.get('__file__')
    if pkg or not file_:
        _log_debug('Package solved or init was called from interactive '
                   'console. __package__=%r, __file__=%r' % (pkg, file_))
        return
    try:
        _solve_pkg(main_globals)
    except Exception as e:
        _print_exc(e)