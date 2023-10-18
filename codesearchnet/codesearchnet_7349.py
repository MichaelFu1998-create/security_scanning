def _start_http_server():
    """Start the daemon's HTTP server on a separate thread.
    This server is only used for servicing container status
    requests from Dusty's custom 502 page."""
    logging.info('Starting HTTP server at {}:{}'.format(constants.DAEMON_HTTP_BIND_IP,
                                                        constants.DAEMON_HTTP_BIND_PORT))
    thread = threading.Thread(target=http_server.app.run, args=(constants.DAEMON_HTTP_BIND_IP,
                                                                constants.DAEMON_HTTP_BIND_PORT))
    thread.daemon = True
    thread.start()