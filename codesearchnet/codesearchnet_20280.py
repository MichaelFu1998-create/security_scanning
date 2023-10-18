def rx(self):
        """
        Receive a series of bytes that have been verified
        :return: a series of bytes as a tuple or None if empty
        """
        if not self._threaded:
            self.run()

        try:
            return tuple(self._messages.pop(0))
        except IndexError:
            return None