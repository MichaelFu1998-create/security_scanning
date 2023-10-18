def contains(self, items, pad=0):
        """
        Test whether coordinates are contained within this tile.

        Parameters
        ----------
        items : ndarray [3] or [N, 3]
            N coordinates to check are within the bounds of the tile

        pad : integer or ndarray [3]
            anisotropic padding to apply in the contain test

        Examples
        --------
        >>> Tile(5, dim=2).contains([[-1, 0], [2, 3], [2, 6]])
        array([False,  True, False], dtype=bool)
        """
        o = ((items >= self.l-pad) & (items < self.r+pad))
        if len(o.shape) == 2:
            o = o.all(axis=-1)
        elif len(o.shape) == 1:
            o = o.all()
        return o