def rotation(self, rotation):
        '''Set the rotation of this body using a rotation matrix.

        Parameters
        ----------
        rotation : sequence of 9 floats
            The desired rotation matrix for this body.
        '''
        if isinstance(rotation, np.ndarray):
            rotation = rotation.ravel()
        self.ode_body.setRotation(tuple(rotation))