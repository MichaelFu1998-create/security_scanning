def serve_forever_stoppable(self):
        """Handle one request at a time until stop_serve_forever().

        http://code.activestate.com/recipes/336012/
        """
        self.stop_request = False
        self.stopped = False

        while not self.stop_request:
            self.handle_request()

        #        _logger.info "serve_forever_stoppable() stopped."
        self.stopped = True