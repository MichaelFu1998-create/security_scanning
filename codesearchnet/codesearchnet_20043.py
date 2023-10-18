def add_listener(self, event, listener):
        """Bind a listener to a particular event.

        Args:
            event (str): The name of the event to listen for. This may be any
                string value.
            listener (def or async def): The callback to execute when the event
                fires. This may be a sync or async function.
        """
        self.emit('new_listener', event, listener)
        self._listeners[event].append(listener)
        self._check_limit(event)
        return self