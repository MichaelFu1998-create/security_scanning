def wait_for_writability(self):
        """
        Stop current thread until the channel is writable.

        :Return: `False` if it won't be readable (e.g. is closed)
        """
        with self.lock:
            while True:
                if self._state in ("closing", "closed", "aborted"):
                    return False
                if self._socket and bool(self._write_queue):
                    return True
                self._write_queue_cond.wait()
        return False