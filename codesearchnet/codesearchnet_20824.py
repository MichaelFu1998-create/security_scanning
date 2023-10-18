def create_body(self, shape, name=None, **kwargs):
        '''Create a new body.

        Parameters
        ----------
        shape : str
            The "shape" of the body to be created. This should name a type of
            body object, e.g., "box" or "cap".
        name : str, optional
            The name to use for this body. If not given, a default name will be
            constructed of the form "{shape}{# of objects in the world}".

        Returns
        -------
        body : :class:`Body`
            The created body object.
        '''
        shape = shape.lower()
        if name is None:
            for i in range(1 + len(self._bodies)):
                name = '{}{}'.format(shape, i)
                if name not in self._bodies:
                    break
        self._bodies[name] = Body.build(shape, name, self, **kwargs)
        return self._bodies[name]