def peek(self, eof_token=False):
        """Same as :meth:`next`, except the token is not dequeued."""
        if len(self.queue) == 0:
            self._refill(eof_token)

        return self.queue[-1]