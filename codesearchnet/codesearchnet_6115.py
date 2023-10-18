def _run_cheroot(app, config, mode):
    """Run WsgiDAV using cheroot.server if Cheroot is installed."""
    assert mode == "cheroot"
    try:
        from cheroot import server, wsgi
    #         from cheroot.ssl.builtin import BuiltinSSLAdapter
    #         import cheroot.ssl.pyopenssl
    except ImportError:
        _logger.error("*" * 78)
        _logger.error("ERROR: Could not import Cheroot.")
        _logger.error(
            "Try `pip install cheroot` or specify another server using the --server option."
        )
        _logger.error("*" * 78)
        raise

    server_name = "WsgiDAV/{} {} Python/{}".format(
        __version__, wsgi.Server.version, util.PYTHON_VERSION
    )
    wsgi.Server.version = server_name

    # Support SSL
    ssl_certificate = _get_checked_path(config.get("ssl_certificate"), config)
    ssl_private_key = _get_checked_path(config.get("ssl_private_key"), config)
    ssl_certificate_chain = _get_checked_path(
        config.get("ssl_certificate_chain"), config
    )
    ssl_adapter = config.get("ssl_adapter", "builtin")
    protocol = "http"
    if ssl_certificate and ssl_private_key:
        ssl_adapter = server.get_ssl_adapter_class(ssl_adapter)
        wsgi.Server.ssl_adapter = ssl_adapter(
            ssl_certificate, ssl_private_key, ssl_certificate_chain
        )
        protocol = "https"
        _logger.info("SSL / HTTPS enabled. Adapter: {}".format(ssl_adapter))
    elif ssl_certificate or ssl_private_key:
        raise RuntimeError(
            "Option 'ssl_certificate' and 'ssl_private_key' must be used together."
        )
    #     elif ssl_adapter:
    #         print("WARNING: Ignored option 'ssl_adapter' (requires 'ssl_certificate').")

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

    server = wsgi.Server(**server_args)

    # If the caller passed a startup event, monkey patch the server to set it
    # when the request handler loop is entered
    startup_event = config.get("startup_event")
    if startup_event:

        def _patched_tick():
            server.tick = org_tick  # undo the monkey patch
            _logger.info("wsgi.Server is ready")
            startup_event.set()
            org_tick()

        org_tick = server.tick
        server.tick = _patched_tick

    try:
        server.start()
    except KeyboardInterrupt:
        _logger.warning("Caught Ctrl-C, shutting down...")
    finally:
        server.stop()

    return