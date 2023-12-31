def serve(self, sock, request_handler, error_handler, debug=False,
              request_timeout=60, ssl=None, request_max_size=None,
              reuse_port=False, loop=None, protocol=HttpProtocol,
              backlog=100, **kwargs):
        """Start asynchronous HTTP Server on an individual process.

        :param request_handler: Sanic request handler with middleware
        :param error_handler: Sanic error handler with middleware
        :param debug: enables debug output (slows server)
        :param request_timeout: time in seconds
        :param ssl: SSLContext
        :param sock: Socket for the server to accept connections from
        :param request_max_size: size in bytes, `None` for no limit
        :param reuse_port: `True` for multiple workers
        :param loop: asyncio compatible event loop
        :param protocol: subclass of asyncio protocol class
        :return: Nothing
        """
        if debug:
            loop.set_debug(debug)

        server = partial(
            protocol,
            loop=loop,
            connections=self.connections,
            signal=self.signal,
            request_handler=request_handler,
            error_handler=error_handler,
            request_timeout=request_timeout,
            request_max_size=request_max_size,
        )

        server_coroutine = loop.create_server(
            server,
            host=None,
            port=None,
            ssl=ssl,
            reuse_port=reuse_port,
            sock=sock,
            backlog=backlog
        )
        # Instead of pulling time at the end of every request,
        # pull it once per minute
        loop.call_soon(partial(update_current_time, loop))
        return server_coroutine