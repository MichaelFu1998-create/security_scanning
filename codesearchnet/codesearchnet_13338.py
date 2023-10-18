def _timeout_cb(self, method):
        """Call the timeout handler due.
        """
        self._anything_done = True
        logger.debug("_timeout_cb() called for: {0!r}".format(method))
        result = method()
        # pylint: disable=W0212
        rec = method._pyxmpp_recurring
        if rec:
            self._prepare_pending()
            return True

        if rec is None and result is not None:
            logger.debug(" auto-recurring, restarting in {0} s"
                                                            .format(result))
            tag = glib.timeout_add(int(result * 1000), self._timeout_cb, method)
            self._timer_sources[method] = tag
        else:
            self._timer_sources.pop(method, None)
        self._prepare_pending()
        return False