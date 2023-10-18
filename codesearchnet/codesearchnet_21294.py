def serve_forever(self, poll_interval=0.5):
        """
        Start serving HTTP requests

        This method blocks the current thread.

        :param poll_interval: polling timeout
        :return:
        """
        logger.info('Starting server on {}:{}...'.format(
            self.server_name, self.server_port)
        )
        while True:
            try:
                self.poll_once(poll_interval)
            except (KeyboardInterrupt, SystemExit):
                break
        self.handle_close()
        logger.info('Server stopped.')