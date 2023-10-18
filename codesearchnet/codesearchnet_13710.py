def _prepare_handlers(self):
        """Prepare the I/O handlers.

        :Return: (readable, writable, timeout) tuple. 'readable' is the list
            of readable handlers, 'writable' - the list of writable handlers,
            'timeout' the suggested maximum timeout for this loop iteration or
            `None`
        """
        timeout = None
        readable = []
        writable = []
        for handler in self._handlers:
            if handler not in self._prepared:
                logger.debug(" preparing handler: {0!r}".format(handler))
                ret = handler.prepare()
                logger.debug("   prepare result: {0!r}".format(ret))
                if isinstance(ret, HandlerReady):
                    self._prepared.add(handler)
                elif isinstance(ret, PrepareAgain):
                    if ret.timeout is not None:
                        if timeout is None:
                            timeout = ret.timeout
                        else:
                            timeout = min(timeout, ret.timeout)
                else:
                    raise TypeError("Unexpected result type from prepare()")
            if not handler.fileno():
                logger.debug(" {0!r}: no fileno".format(handler))
                continue
            if handler.is_readable():
                logger.debug(" {0!r} readable".format(handler))
                readable.append(handler)
            if handler.is_writable():
                logger.debug(" {0!r} writable".format(handler))
                writable.append(handler)
        return readable, writable, timeout