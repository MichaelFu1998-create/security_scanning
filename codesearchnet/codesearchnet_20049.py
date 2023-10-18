def _dispatch(self, event, listener, *args, **kwargs):
        """Dispatch an event to a listener.

        Args:
            event (str): The name of the event that triggered this call.
            listener (def or async def): The listener to trigger.
            *args: Any number of positional arguments.
            **kwargs: Any number of keyword arguments.

        This method inspects the listener. If it is a def it dispatches the
        listener to a method that will execute that def. If it is an async def
        it dispatches it to a method that will schedule the resulting coro with
        the event loop.
        """
        if (
            asyncio.iscoroutinefunction(listener) or
            isinstance(listener, functools.partial) and
            asyncio.iscoroutinefunction(listener.func)
        ):

            return self._dispatch_coroutine(event, listener, *args, **kwargs)

        return self._dispatch_function(event, listener, *args, **kwargs)