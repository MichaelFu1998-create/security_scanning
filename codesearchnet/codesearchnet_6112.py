def _run_paste(app, config, mode):
    """Run WsgiDAV using paste.httpserver, if Paste is installed.

    See http://pythonpaste.org/modules/httpserver.html for more options
    """
    from paste import httpserver

    version = "WsgiDAV/{} {} Python {}".format(
        __version__, httpserver.WSGIHandler.server_version, util.PYTHON_VERSION
    )
    _logger.info("Running {}...".format(version))

    # See http://pythonpaste.org/modules/httpserver.html for more options
    server = httpserver.serve(
        app,
        host=config["host"],
        port=config["port"],
        server_version=version,
        # This option enables handling of keep-alive
        # and expect-100:
        protocol_version="HTTP/1.1",
        start_loop=False,
    )

    if config["verbose"] >= 5:
        __handle_one_request = server.RequestHandlerClass.handle_one_request

        def handle_one_request(self):
            __handle_one_request(self)
            if self.close_connection == 1:
                _logger.debug("HTTP Connection : close")
            else:
                _logger.debug("HTTP Connection : continue")

        server.RequestHandlerClass.handle_one_request = handle_one_request

        # __handle = server.RequestHandlerClass.handle

        # def handle(self):
        #     _logger.debug("open HTTP connection")
        #     __handle(self)

        server.RequestHandlerClass.handle_one_request = handle_one_request

    host, port = server.server_address
    if host == "0.0.0.0":
        _logger.info(
            "Serving on 0.0.0.0:{} view at {}://127.0.0.1:{}".format(port, "http", port)
        )
    else:
        _logger.info("Serving on {}://{}:{}".format("http", host, port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        _logger.warning("Caught Ctrl-C, shutting down...")
    return