def _prepare_io_handler(self, handler):
        """Call the `interfaces.IOHandler.prepare` method and
        remove the handler from unprepared handler list when done.
        """
        logger.debug(" preparing handler: {0!r}".format(handler))
        ret = handler.prepare()
        logger.debug("   prepare result: {0!r}".format(ret))
        if isinstance(ret, HandlerReady):
            del self._unprepared_handlers[handler]
            prepared = True
        elif isinstance(ret, PrepareAgain):
            if ret.timeout is not None:
                now = time.time()
                self.io_loop.add_timeout(
                    now + ret.timeout,
                    partial(self._configure_io_handler, handler)
                )
            else:
                self.io_loop.add_callback(
                    partial(self._configure_io_handler, handler)
                )
            prepared = False
        else:
            raise TypeError("Unexpected result type from prepare()")
        return prepared