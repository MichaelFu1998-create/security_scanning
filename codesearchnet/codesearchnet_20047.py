def _dispatch_coroutine(self, event, listener, *args, **kwargs):
        """Schedule a coroutine for execution.

        Args:
            event (str): The name of the event that triggered this call.
            listener (async def): The async def that needs to be executed.
            *args: Any number of positional arguments.
            **kwargs: Any number of keyword arguments.

        The values of *args and **kwargs are passed, unaltered, to the async
        def when generating the coro. If there is an exception generating the
        coro, such as the wrong number of arguments, the emitter's error event
        is triggered. If the triggering event _is_ the emitter's error event
        then the exception is reraised. The reraised exception may show in
        debug mode for the event loop but is otherwise silently dropped.
        """
        try:

            coro = listener(*args, **kwargs)

        except Exception as exc:

            if event == self.LISTENER_ERROR_EVENT:

                raise

            return self.emit(self.LISTENER_ERROR_EVENT, event, listener, exc)

        asyncio.ensure_future(
            _try_catch_coro(self, event, listener, coro),
            loop=self._loop,
        )