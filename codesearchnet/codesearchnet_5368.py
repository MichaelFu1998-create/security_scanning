def listen(self, callback, *args, **kwargs):
        """
        Like :class:`connect()`, but uses a weak reference instead of a
        normal reference.
        The signal is automatically disconnected as soon as the handler
        is garbage collected.

        .. note::

            Storing signal handlers as weak references means that if
            your handler is a local function, it may be garbage collected. To
            prevent this, use :class:`connect()` instead.

        :type  callback: object
        :param callback: The callback function.
        :type  args: tuple
        :param args: Optional arguments passed to the callback.
        :type  kwargs: dict
        :param kwargs: Optional keyword arguments passed to the callback.
        :rtype:  :class:`Exscript.util.weakmethod.WeakMethod`
        :returns: The newly created weak reference to the callback.
        """
        if self.lock is None:
            self.lock = Lock()
        with self.lock:
            if self.is_connected(callback):
                raise AttributeError('callback is already connected')
            if self.weak_subscribers is None:
                self.weak_subscribers = []
            ref = weakmethod.ref(callback, self._try_disconnect)
            self.weak_subscribers.append((ref, args, kwargs))
        return ref