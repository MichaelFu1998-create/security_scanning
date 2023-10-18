def hold_exception(method):
    """Decorator for glib callback methods of GLibMainLoop used to store the
    exception raised."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper for methods decorated with `hold_exception`."""
        # pylint: disable=W0703,W0212
        try:
            return method(self, *args, **kwargs)
        except Exception:
            if self.exc_info:
                raise
            if not self._stack:
                logger.debug('@hold_exception wrapped method {0!r} called'
                            ' from outside of the main loop'.format(method))
                raise
            self.exc_info = sys.exc_info()
            logger.debug(u"exception in glib main loop callback:",
                                                exc_info = self.exc_info)
            # pylint: disable=W0212
            main_loop = self._stack[-1]
            if main_loop is not None:
                main_loop.quit()
            return False
    return wrapper