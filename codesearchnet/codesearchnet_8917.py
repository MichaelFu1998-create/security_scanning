def find(self, s):
        """Locates the leader of the set to which the element ``s`` belongs.

        Parameters
        ----------
        s : object
            An object that the ``UnionFind`` contains.

        Returns
        -------
        object
            The leader of the set that contains ``s``.
        """
        pSet   = [s]
        parent = self._leader[s]

        while parent != self._leader[parent]:
            pSet.append(parent)
            parent = self._leader[parent]

        if len(pSet) > 1:
            for a in pSet:
                self._leader[a] = parent

        return parent