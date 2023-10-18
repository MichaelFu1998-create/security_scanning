def _run__cherrypy(app, config, mode):
    """Run WsgiDAV using cherrypy.wsgiserver if CherryPy is installed."""
    assert mode == "cherrypy-wsgiserver"

    try:
        from cherrypy import wsgiserver
        from cherrypy.wsgiserver.ssl_builtin import BuiltinSSLAdapter

        _logger.warning("WARNING: cherrypy.wsgiserver is deprecated.")
        _logger.warning(
            "         Starting with CherryPy 9.0 the functionality from cherrypy.wsgiserver"
        )
        _logger.warning("         was moved to the cheroot project.")
        _logger.warning("         Consider using --server=cheroot.")
    except ImportError:
        _logger.error("*" * 78)
        _logger.error("ERROR: Could not import cherrypy.wsgiserver.")
        _logger.error(
            "Try `pip install cherrypy` or specify another server using the --server option."
        )
        _logger.error("Note that starting with CherryPy 9.0, the server was moved to")
        _logger.error(
            "the cheroot project, so it is recommended to use `-server=cheroot`"
        )
        _logger.error("and run `pip install cheroot` instead.")
        _logger.error("*" * 78)
        raise

    server_name = "WsgiDAV/{} {} Python/{}".format(
        __version__, wsgiserver.CherryPyWSGIServer.version, util.PYTHON_VERSION
    )
    wsgiserver.CherryPyWSGIServer.version = server_name

    # Support SSL
    ssl_certificate = _get_checked_path(config.get("ssl_certificate"), config)
    ssl_private_key = _get_checked_path(config.get("ssl_private_key"), config)
    ssl_certificate_chain = _get_checked_path(
        config.get("ssl_certificate_chain"), config
    )
    protocol = "http"
    if ssl_certificate:
        assert ssl_private_key
        wsgiserver.CherryPyWSGIServer.ssl_adapter = BuiltinSSLAdapter(
            ssl_certificate, ssl_private_key, ssl_certificate_chain
        )
        protocol = "https"
        _logger.info("SSL / HTTPS enabled.")

    _logger.info("Running {}".format(server_name))
    _logger.info(
        "Serving on {}://{}:{} ...".format(protocol, config["host"], config["port"])
    )

    server_args = {
        "bind_addr": (config["host"], config["port"]),
        "wsgi_app": app,
        "server_name": server_name,
    }
    # Override or add custom args
    server_args.update(config.get("server_args", {}))

    server = wsgiserver.CherryPyWSGIServer(**server_args)

    # If the caller passed a startup event, monkey patch the server to set it
    # when the request handler loop is entered
    startup_event = config.get("startup_event")
    if startup_event:

        def _patched_tick():
            server.tick = org_tick  # undo the monkey patch
            org_tick()
            _logger.info("CherryPyWSGIServer is ready")
            startup_event.set()

        org_tick = server.tick
        server.tick = _patched_tick

    try:
        server.start()
    except KeyboardInterrupt:
        _logger.warning("Caught Ctrl-C, shutting down...")
    finally:
        server.stop()
    return