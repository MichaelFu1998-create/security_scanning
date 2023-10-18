def make_server(host, port, app=None,
                server_class=AsyncWsgiServer,
                handler_class=AsyncWsgiHandler,
                ws_handler_class=None,
                ws_path='/ws'):
    """Create server instance with an optional WebSocket handler

    For pure WebSocket server ``app`` may be ``None`` but an attempt to access
    any path other than ``ws_path`` will cause server error.
    
    :param host: hostname or IP
    :type host: str
    :param port: server port
    :type port: int
    :param app: WSGI application
    :param server_class: WSGI server class, defaults to AsyncWsgiServer
    :param handler_class: WSGI handler class, defaults to AsyncWsgiHandler
    :param ws_handler_class: WebSocket hanlder class, defaults to ``None``
    :param ws_path: WebSocket path on the server, defaults to '/ws'
    :type ws_path: str, optional
    :return: initialized server instance
    """
    handler_class.ws_handler_class = ws_handler_class
    handler_class.ws_path = ws_path
    httpd = server_class((host, port), RequestHandlerClass=handler_class)
    httpd.set_app(app)
    return httpd