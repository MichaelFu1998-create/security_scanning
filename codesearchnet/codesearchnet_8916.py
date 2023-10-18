def size(self, s):
        """Returns the number of elements in the set that ``s`` belongs to.

        Parameters
        ----------
        s : object
            An object

        Returns
        -------
        out : int
            The number of elements in the set that ``s`` belongs to.
        """
        leader = self.find(s)
        return self._size[leader]