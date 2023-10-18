def _call_timeout_handlers(self):
        """Call the timeout handlers due.

        :Return: (next_event_timeout, sources_handled) tuple.
            next_event_timeout is number of seconds until the next timeout
            event, sources_handled is number of handlers called.
        """
        sources_handled = 0
        now = time.time()
        schedule = None
        while self._timeout_handlers:
            schedule, handler = self._timeout_handlers[0]
            if schedule <= now:
                # pylint: disable-msg=W0212
                logger.debug("About to call a timeout handler: {0!r}"
                                                        .format(handler))
                self._timeout_handlers = self._timeout_handlers[1:]
                result = handler()
                logger.debug(" handler result: {0!r}".format(result))
                rec = handler._pyxmpp_recurring
                if rec:
                    logger.debug(" recurring, restarting in {0} s"
                                        .format(handler._pyxmpp_timeout))
                    self._timeout_handlers.append(
                                    (now + handler._pyxmpp_timeout, handler))
                    self._timeout_handlers.sort(key = lambda x: x[0])
                elif rec is None and result is not None:
                    logger.debug(" auto-recurring, restarting in {0} s"
                                                            .format(result))
                    self._timeout_handlers.append((now + result, handler))
                    self._timeout_handlers.sort(key = lambda x: x[0])
                sources_handled += 1
            else:
                break
            if self.check_events():
                return 0, sources_handled
        if self._timeout_handlers and schedule:
            timeout = schedule - now
        else:
            timeout = None
        return timeout, sources_handled