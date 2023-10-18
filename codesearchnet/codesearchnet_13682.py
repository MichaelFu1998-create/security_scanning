def _handle_event(self, handler, fd, event):
        """handle I/O events"""
        # pylint: disable=C0103
        logger.debug('_handle_event: %r, %r, %r', handler, fd, event)
        if event & ioloop.IOLoop.ERROR:
            handler.handle_hup()
        if event & ioloop.IOLoop.READ:
            handler.handle_read()
        if event & ioloop.IOLoop.WRITE:
            handler.handle_write()
        self._configure_io_handler(handler)