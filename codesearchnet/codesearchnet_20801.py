def relative_offset_to_world(self, offset):
        '''Convert a relative body offset to world coordinates.

        Parameters
        ----------
        offset : 3-tuple of float
            The offset of the desired point, given as a relative fraction of the
            size of this body. For example, offset (0, 0, 0) is the center of
            the body, while (0.5, -0.2, 0.1) describes a point halfway from the
            center towards the maximum x-extent of the body, 20% of the way from
            the center towards the minimum y-extent, and 10% of the way from the
            center towards the maximum z-extent.

        Returns
        -------
        position : 3-tuple of float
            A position in world coordinates of the given body offset.
        '''
        return np.array(self.body_to_world(offset * self.dimensions / 2))