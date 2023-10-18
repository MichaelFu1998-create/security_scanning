def _prepare_io_handler(self, handler):
        """Call the `interfaces.IOHandler.prepare` method and
        remove the handler from unprepared handler list when done.
        """
        logger.debug(" preparing handler: {0!r}".format(handler))
        self._unprepared_pending.discard(handler)
        ret = handler.prepare()
        logger.debug("   prepare result: {0!r}".format(ret))
        if isinstance(ret, HandlerReady):
            del self._unprepared_handlers[handler]
            prepared = True
        elif isinstance(ret, PrepareAgain):
            if ret.timeout == 0:
                tag = glib.idle_add(self._prepare_io_handler_cb, handler)
                self._prepare_sources[handler] = tag
            elif ret.timeout is not None:
                timeout = ret.timeout
                timeout = int(timeout * 1000)
                if not timeout:
                    timeout = 1
                tag = glib.timeout_add(timeout, self._prepare_io_handler_cb,
                                                                    handler)
                self._prepare_sources[handler] = tag
            else:
                self._unprepared_pending.add(handler)
            prepared = False
        else:
            raise TypeError("Unexpected result type from prepare()")
        return prepared