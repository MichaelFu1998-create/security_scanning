def loop_iteration(self, timeout = 0.1):
        """Wait up to `timeout` seconds, raise any exception from the
        threads.
        """
        try:
            exc_info = self.exc_queue.get(True, timeout)[1]
        except Queue.Empty:
            return
        exc_type, exc_value, ext_stack = exc_info
        raise exc_type, exc_value, ext_stack