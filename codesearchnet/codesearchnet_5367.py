def connect(self, callback, *args, **kwargs):
        """
        Connects the event with the given callback.
        When the signal is emitted, the callback is invoked.

        .. note::

            The signal handler is stored with a hard reference, so you
            need to make sure to call :class:`disconnect()` if you want the
            handler
            to be garbage collected.

        :type  callback: object
        :param callback: The callback function.
        :type  args: tuple
        :param args: Optional arguments passed to the callback.
        :type  kwargs: dict
        :param kwargs: Optional keyword arguments passed to the callback.
        """
        if self.is_connected(callback):
            raise AttributeError('callback is already connected')
        if self.hard_subscribers is None:
            self.hard_subscribers = []
        self.hard_subscribers.append((callback, args, kwargs))