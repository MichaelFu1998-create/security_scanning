def body_to_world(self, position):
        '''Convert a body-relative offset to world coordinates.

        Parameters
        ----------
        position : 3-tuple of float
            A tuple giving body-relative offsets.

        Returns
        -------
        position : 3-tuple of float
            A tuple giving the world coordinates of the given offset.
        '''
        return np.array(self.ode_body.getRelPointPos(tuple(position)))