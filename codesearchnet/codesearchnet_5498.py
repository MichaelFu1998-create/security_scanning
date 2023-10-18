def cmd_daemon(opts):
    """Start the Blockade REST API
    """
    if opts.data_dir is None:
        raise BlockadeError("You must supply a data directory for the daemon")
    rest.start(data_dir=opts.data_dir, port=opts.port, debug=opts.debug,
        host_exec=get_host_exec())