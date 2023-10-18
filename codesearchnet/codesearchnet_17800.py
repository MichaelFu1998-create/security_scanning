def from_curvilinear(cls, x, y, z, formatter=numpy_formatter):
        """Construct a contour generator from a curvilinear grid.

        Note
        ----
        This is an alias for the default constructor.

        Parameters
        ----------
        x : array_like
            x coordinates of each point in `z`.  Must be the same size as `z`.
        y : array_like
            y coordinates of each point in `z`.  Must be the same size as `z`.
        z : array_like
            The 2-dimensional curvilinear grid of data to compute
            contours for.  Masked arrays are supported.
        formatter : callable
            A conversion function to convert from the internal `Matplotlib`_
            contour format to an external format.  See :ref:`formatters` for
            more information.

        Returns
        -------
        : :class:`QuadContourGenerator`
            Initialized contour generator.

        """
        return cls(x, y, z, formatter)