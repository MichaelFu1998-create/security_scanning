def _exception_handler(self, _loop, context):
        """Handle exceptions from the asyncio loop."""
        # Start a graceful shutdown.
        self._coroutine_queue.put(self._client.disconnect())

        # Store the exception to be re-raised later. If the context doesn't
        # contain an exception, create one containing the error message.
        default_exception = Exception(context.get('message'))
        self._exception = context.get('exception', default_exception)