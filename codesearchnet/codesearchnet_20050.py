def emit(self, event, *args, **kwargs):
        """Call each listener for the event with the given arguments.

        Args:
            event (str): The event to trigger listeners on.
            *args: Any number of positional arguments.
            **kwargs: Any number of keyword arguments.

        This method passes all arguments other than the event name directly
        to the listeners. If a listener raises an exception for any reason the
        'listener-error', or current value of LISTENER_ERROR_EVENT, is emitted.
        Listeners to this event are given the event name, listener object, and
        the exception raised. If an error listener fails it does so silently.

        All event listeners are fired in a deferred way so this method returns
        immediately. The calling coro must yield at some point for the event
        to propagate to the listeners.
        """
        listeners = self._listeners[event]
        listeners = itertools.chain(listeners, self._once[event])
        self._once[event] = []
        for listener in listeners:

            self._loop.call_soon(
                functools.partial(
                    self._dispatch,
                    event,
                    listener,
                    *args,
                    **kwargs,
                )
            )

        return self