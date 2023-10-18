def stop_serve_forever(self):
        """Stop serve_forever_stoppable()."""
        assert hasattr(
            self, "stop_request"
        ), "serve_forever_stoppable() must be called before"
        assert not self.stop_request, "stop_serve_forever() must only be called once"

        #        # Flag stop request
        self.stop_request = True
        time.sleep(0.1)
        if self.stopped:
            # _logger.info "stop_serve_forever() 'stopped'."
            return

        # Add a do_SHUTDOWN method to to the ExtHandler class
        def _shutdownHandler(self):
            """Send 200 OK response, and set server.stop_request to True.

            http://code.activestate.com/recipes/336012/
            """
            #            _logger.info "Handling do_SHUTDOWN request"
            self.send_response(200)
            self.end_headers()
            self.server.stop_request = True

        if not hasattr(ExtHandler, "do_SHUTDOWN"):
            ExtHandler.do_SHUTDOWN = _shutdownHandler

        # Send request, so socket is unblocked
        (host, port) = self.server_address
        #        _logger.info "stop_serve_forever() sending {}:{}/ SHUTDOWN...".format(host, port)
        conn = http_client.HTTPConnection("{}:{}".format(host, port))
        conn.request("SHUTDOWN", "/")
        #        _logger.info "stop_serve_forever() sent SHUTDOWN request, reading response..."
        conn.getresponse()
        #        _logger.info "stop_serve_forever() received SHUTDOWN response."
        assert self.stop_request