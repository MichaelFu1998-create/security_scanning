def world_to_body(self, position):
        '''Convert a point in world coordinates to a body-relative offset.

        Parameters
        ----------
        position : 3-tuple of float
            A world coordinates position.

        Returns
        -------
        offset : 3-tuple of float
            A tuple giving the body-relative offset of the given position.
        '''
        return np.array(self.ode_body.getPosRelPoint(tuple(position)))