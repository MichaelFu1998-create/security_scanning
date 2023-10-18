def get(self, timeout=None):
        """
        Return value on success, or raise exception on failure.
        """
        result = None
        try:
            result = self._result.get(True, timeout=timeout)
        except Empty:
            raise Timeout()

        if isinstance(result, Failure):
            six.reraise(*result.exc_info)
        else:
            return result