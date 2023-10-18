def dispatch(self, block = False, timeout = None):
        """Get the next event from the queue and pass it to
        the appropriate handlers.

        :Parameters:
            - `block`: wait for event if the queue is empty
            - `timeout`: maximum time, in seconds, to wait if `block` is `True`
        :Types:
            - `block`: `bool`
            - `timeout`: `float`

        :Return: the event handled (may be `QUIT`) or `None`
        """
        logger.debug(" dispatching...")
        try:
            event = self.queue.get(block, timeout)
        except Queue.Empty:
            logger.debug("    queue empty")
            return None
        try:
            logger.debug("    event: {0!r}".format(event))
            if event is QUIT:
                return QUIT
            handlers = list(self._handler_map[None])
            klass = event.__class__
            if klass in self._handler_map:
                handlers += self._handler_map[klass]
            logger.debug("    handlers: {0!r}".format(handlers))
            # to restore the original order of handler objects
            handlers.sort(key = lambda x: x[0])
            for dummy, handler in handlers:
                logger.debug(u"  passing the event to: {0!r}".format(handler))
                result = handler(event)
                if isinstance(result, Event):
                    self.queue.put(result)
                elif result and event is not QUIT:
                    return event
            return event
        finally:
            self.queue.task_done()