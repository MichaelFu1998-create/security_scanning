def listen(self, func):
        """
        Listen to parameters change.

        Parameters
        ----------
        func : callable
            Function to be called when a parameter changes.
        """
        self._C0.listen(func)
        self._C1.listen(func)