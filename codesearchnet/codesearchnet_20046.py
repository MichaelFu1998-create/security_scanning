def remove_all_listeners(self, event=None):
        """Remove all listeners, or those of the specified *event*.

        It's not a good idea to remove listeners that were added elsewhere in
        the code, especially when it's on an emitter that you didn't create
        (e.g. sockets or file streams).
        """
        if event is None:
            self._listeners = collections.defaultdict(list)
            self._once = collections.defaultdict(list)
        else:
            del self._listeners[event]
            del self._once[event]