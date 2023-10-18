def update(self, params, values):
        """
        Update a single parameter or group of parameters ``params``
        with ``values``.

        Parameters
        ----------
        params : string or list of strings
            Parameter names which to update

        value : number or list of numbers
            Values of those parameters which to update
        """
        return super(State, self).update(params, values)