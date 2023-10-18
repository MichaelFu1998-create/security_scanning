def spend_key(self):
        """
        Returns private spend key. None if wallet is view-only.

        :rtype: str or None
        """
        key = self._backend.spend_key()
        if key == numbers.EMPTY_KEY:
            return None
        return key