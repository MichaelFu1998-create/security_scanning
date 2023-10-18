def _run_gevent(app, config, mode):
    """Run WsgiDAV using gevent if gevent is installed.

    See
      https://github.com/gevent/gevent/blob/master/src/gevent/pywsgi.py#L1356
      https://github.com/gevent/gevent/blob/master/src/gevent/server.py#L38
     for more options
    """
    import gevent
    import gevent.monkey

    gevent.monkey.patch_all()
    from gevent.pywsgi import WSGIServer

    server_args = {
        "bind_addr": (config["host"], config["port"]),
        "wsgi_app": app,
        # TODO: SSL support
        "keyfile": None,
        "certfile": None,
    }
    protocol = "http"
    # Override or add custom args
    server_args.update(config.get("server_args", {}))

    dav_server = WSGIServer(server_args["bind_addr"], app)
    _logger.info("Running {}".format(dav_server))
    _logger.info(
        "Serving on {}://{}:{} ...".format(protocol, config["host"], config["port"])
    )
    try:
        gevent.spawn(dav_server.serve_forever())
    except KeyboardInterrupt:
        _logger.warning("Caught Ctrl-C, shutting down...")
    return