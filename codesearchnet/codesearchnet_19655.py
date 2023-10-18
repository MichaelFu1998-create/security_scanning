def run_server(self, port):
        """run a server binding to port"""

        try:
            self.server = MultiThreadedHTTPServer(('0.0.0.0', port), Handler)
        except socket.error, e:  # failed to bind port
            logger.error(str(e))
            sys.exit(1)

        logger.info("HTTP serve at http://0.0.0.0:%d (ctrl-c to stop) ..."
                    % port)

        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            logger.info("^C received, shutting down server")
            self.shutdown_server()