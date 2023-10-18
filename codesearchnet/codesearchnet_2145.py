def _next_position_then_increment(self):
        """
        Similar to position++.
        """
        start = self._capacity - 1
        position = start + self._position
        self._position = (self._position + 1) % self._capacity
        return position