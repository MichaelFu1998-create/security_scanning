def parent_callback(self, executor_fu):
        """Callback from a parent future to update the AppFuture.

        Used internally by AppFuture, and should not be called by code using AppFuture.

        Args:
            - executor_fu (Future): Future returned by the executor along with callback.
              This may not be the current parent future, as the parent future may have
              already been updated to point to a retrying execution, and in that case,
              this is logged.

              In the case that a new parent has been attached, we must immediately discard
              this result no matter what it contains (although it might be interesting
              to log if it was successful...)

        Returns:
            - None

        Updates the super() with the result() or exception()
        """
        with self._update_lock:

            if not executor_fu.done():
                raise ValueError("done callback called, despite future not reporting itself as done")

            # this is for consistency checking
            if executor_fu != self.parent:
                if executor_fu.exception() is None and not isinstance(executor_fu.result(), RemoteExceptionWrapper):
                    # ... then we completed with a value, not an exception or wrapped exception,
                    # but we've got an updated executor future.
                    # This is bad - for example, we've started a retry even though we have a result

                    raise ValueError("internal consistency error: AppFuture done callback called without an exception, but parent has been changed since then")

            try:
                res = executor_fu.result()
                if isinstance(res, RemoteExceptionWrapper):
                    res.reraise()
                super().set_result(executor_fu.result())

            except Exception as e:
                if executor_fu.retries_left > 0:
                    # ignore this exception, because assume some later
                    # parent executor, started external to this class,
                    # will provide the answer
                    pass
                else:
                    super().set_exception(e)