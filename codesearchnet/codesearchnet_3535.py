def _get_id(self):
        """
        Get a unique state id.

        :rtype: int
        """
        id_ = self._last_id.value
        self._last_id.value += 1
        return id_