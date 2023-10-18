def _run_flup(app, config, mode):
    """Run WsgiDAV using flup.server.fcgi if Flup is installed."""
    # http://trac.saddi.com/flup/wiki/FlupServers
    if mode == "flup-fcgi":
        from flup.server.fcgi import WSGIServer, __version__ as flupver
    elif mode == "flup-fcgi-fork":
        from flup.server.fcgi_fork import WSGIServer, __version__ as flupver
    else:
        raise ValueError

    _logger.info(
        "Running WsgiDAV/{} {}/{}...".format(
            __version__, WSGIServer.__module__, flupver
        )
    )
    server = WSGIServer(
        app,
        bindAddress=(config["host"], config["port"]),
        # debug=True,
    )
    try:
        server.run()
    except KeyboardInterrupt:
        _logger.warning("Caught Ctrl-C, shutting down...")
    return