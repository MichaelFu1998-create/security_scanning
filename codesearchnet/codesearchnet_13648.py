def run(self):
        """The thread function.

        Loop waiting for the handler and socket being writable and calling
        `interfaces.IOHandler.handle_write`.
        """
        while not self._quit:
            interval = self.settings["poll_interval"]
            if self.io_handler.is_writable():
                logger.debug("{0}: writable".format(self.name))
                fileno = self.io_handler
                if fileno:
                    writable = wait_for_write(fileno, interval)
                    if writable:
                        self.io_handler.handle_write()
            else:
                logger.debug("{0}: waiting for writaility".format(self.name))
                if not self.io_handler.wait_for_writability():
                    break