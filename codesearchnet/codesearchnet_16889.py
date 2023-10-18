def regular_polygon(cls, center, radius, n_vertices, start_angle=0, **kwargs):
        """Construct a regular polygon.

        Parameters
        ----------
        center : array-like
        radius : float
        n_vertices : int
        start_angle : float, optional
            Where to put the first point, relative to `center`,
            in radians counter-clockwise starting from the horizontal axis.
        kwargs
            Other keyword arguments are passed to the |Shape| constructor.

        """
        angles = (np.arange(n_vertices) * 2 * np.pi / n_vertices) + start_angle
        return cls(center + radius * np.array([np.cos(angles), np.sin(angles)]).T, **kwargs)