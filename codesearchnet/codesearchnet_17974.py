def slicer(self):
        """
        Array slicer object for this tile

        >>> Tile((2,3)).slicer
        (slice(0, 2, None), slice(0, 3, None))

        >>> np.arange(10)[Tile((4,)).slicer]
        array([0, 1, 2, 3])
        """
        return tuple(np.s_[l:r] for l,r in zip(*self.bounds))