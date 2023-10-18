def handle_error(self, request, client_address):
        """Handle an error gracefully.  May be overridden.

        The default is to _logger.info a traceback and continue.

        """
        ei = sys.exc_info()
        e = ei[1]
        # Suppress stack trace when client aborts connection disgracefully:
        # 10053: Software caused connection abort
        # 10054: Connection reset by peer
        if e.args[0] in (10053, 10054):
            _logger.error("*** Caught socket.error: {}".format(e))
            return
        # This is what BaseHTTPServer.HTTPServer.handle_error does, but with
        # added thread ID and using stderr
        _logger.error("-" * 40, file=sys.stderr)
        _logger.error(
            "<{}> Exception happened during processing of request from {}".format(
                threading.currentThread().ident, client_address
            )
        )
        _logger.error(client_address, file=sys.stderr)
        traceback.print_exc()
        _logger.error("-" * 40, file=sys.stderr)
        _logger.error(request, file=sys.stderr)