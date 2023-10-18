def run(self):
        """The thread function.

        First, call the handler's 'prepare' method until it returns
        `HandlerReady` then loop waiting for the socket input and calling
        'handle_read' on the handler.
        """
        # pylint: disable-msg=R0912
        interval = self.settings["poll_interval"]
        prepared = False
        timeout = 0.1
        while not self._quit:
            if not prepared:
                logger.debug("{0}: preparing handler: {1!r}".format(
                                                   self.name, self.io_handler))
                ret = self.io_handler.prepare()
                logger.debug("{0}: prepare result: {1!r}".format(self.name,
                                                                        ret))
                if isinstance(ret, HandlerReady):
                    prepared = True
                elif isinstance(ret, PrepareAgain):
                    if ret.timeout is not None:
                        timeout = ret.timeout
                else:
                    raise TypeError("Unexpected result type from prepare()")
            if self.io_handler.is_readable():
                logger.debug("{0}: readable".format(self.name))
                fileno = self.io_handler.fileno()
                if fileno is not None:
                    readable = wait_for_read(fileno, interval)
                    if readable:
                        self.io_handler.handle_read()
            elif not prepared:
                if timeout:
                    time.sleep(timeout)
            else:
                logger.debug("{0}: waiting for readability".format(self.name))
                if not self.io_handler.wait_for_readability():
                    break