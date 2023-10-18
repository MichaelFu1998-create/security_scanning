def event(self, event): # pylint: disable-msg=R0201
        """Handle a stream event.

        Called when connection state is changed.

        Should not be called with self.lock acquired!
        """
        event.stream = self
        logger.debug(u"Stream event: {0}".format(event))
        self.settings["event_queue"].put(event)
        return False