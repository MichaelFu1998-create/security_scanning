def is_visible(self):
        """:return: is this connection is visible
        :rtype: bool

        A connection is visible if it is longer that 0."""
        if self._start.y + 1 < self._stop.y:
            return True
        return False