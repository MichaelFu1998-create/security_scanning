def indices_for_body(self, name, step=3):
        '''Get a list of the indices for a specific body.

        Parameters
        ----------
        name : str
            The name of the body to look up.
        step : int, optional
            The number of numbers for each body. Defaults to 3, should be set
            to 4 for body rotation (since quaternions have 4 values).

        Returns
        -------
        list of int :
            A list of the index values for quantities related to the named body.
        '''
        for j, body in enumerate(self.bodies):
            if body.name == name:
                return list(range(j * step, (j + 1) * step))
        return []