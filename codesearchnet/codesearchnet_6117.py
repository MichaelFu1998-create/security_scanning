def _run_wsgiref(app, config, mode):
    """Run WsgiDAV using wsgiref.simple_server, on Python 2.5+."""
    # http://www.python.org/doc/2.5.2/lib/module-wsgiref.html
    from wsgiref.simple_server import make_server, software_version

    version = "WsgiDAV/{} {}".format(__version__, software_version)
    _logger.info("Running {}...".format(version))
    _logger.warning(
        "WARNING: This single threaded server (wsgiref) is not meant for production."
    )
    httpd = make_server(config["host"], config["port"], app)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        _logger.warning("Caught Ctrl-C, shutting down...")
    return