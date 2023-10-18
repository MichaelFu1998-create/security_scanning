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
                if self._timeout is not None:
                    self._timeout = min(self._timeout, ret.timeout)
                else:
                    self._timeout = ret.timeout
            prepared = False
        else:
            raise TypeError("Unexpected result type from prepare()")
        return prepared