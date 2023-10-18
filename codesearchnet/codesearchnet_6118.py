def _run_ext_wsgiutils(app, config, mode):
    """Run WsgiDAV using ext_wsgiutils_server from the wsgidav package."""
    from wsgidav.server import ext_wsgiutils_server

    _logger.info(
        "Running WsgiDAV {} on wsgidav.ext_wsgiutils_server...".format(__version__)
    )
    _logger.warning(
        "WARNING: This single threaded server (ext-wsgiutils) is not meant for production."
    )
    try:
        ext_wsgiutils_server.serve(config, app)
    except KeyboardInterrupt:
        _logger.warning("Caught Ctrl-C, shutting down...")
    return