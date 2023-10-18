def marv(ctx, config, loglevel, logfilter, verbosity):
    """Manage a Marv site"""
    if config is None:
        cwd = os.path.abspath(os.path.curdir)
        while cwd != os.path.sep:
            config = os.path.join(cwd, 'marv.conf')
            if os.path.exists(config):
                break
            cwd = os.path.dirname(cwd)
        else:
            config = '/etc/marv/marv.conf'
            if not os.path.exists(config):
                config = None
    ctx.obj = config
    setup_logging(loglevel, verbosity, logfilter)