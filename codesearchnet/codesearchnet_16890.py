def circle(cls, center, radius, n_vertices=50, **kwargs):
        """Construct a circle.

        Parameters
        ----------
        center : array-like
        radius : float
        n_vertices : int, optional
            Number of points to draw.
            Decrease for performance, increase for appearance.
        kwargs
            Other keyword arguments are passed to the |Shape| constructor.

        """
        return cls.regular_polygon(center, radius, n_vertices, **kwargs)