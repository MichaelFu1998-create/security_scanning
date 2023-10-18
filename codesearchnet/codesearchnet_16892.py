def from_dict(cls, spec):
        """Create a |Shape| from a dictionary specification.

        Parameters
        ----------
        spec : dict
            A dictionary with either the fields ``'center'`` and ``'radius'`` (for a circle),
            ``'center'``, ``'radius'``, and ``'n_vertices'`` (for a regular polygon),
            or ``'vertices'``.
            If only two vertices are given, they are assumed to be lower left and top right corners of a rectangle.
            Other fields are interpreted as keyword arguments.

        """
        spec = spec.copy()
        center = spec.pop('center', None)
        radius = spec.pop('radius', None)
        if center and radius:
            return cls.circle(center, radius, **spec)

        vertices = spec.pop('vertices')
        if len(vertices) == 2:
            return cls.rectangle(vertices, **spec)

        return cls(vertices, **spec)