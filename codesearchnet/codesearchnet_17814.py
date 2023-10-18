def filled_contour(self, min=None, max=None):
        """Get contour polygons between the given levels.

        Parameters
        ----------
        min : numbers.Number or None
            The minimum data level of the contour polygon.  If :obj:`None`,
            ``numpy.finfo(numpy.float64).min`` will be used.
        max : numbers.Number or None
            The maximum data level of the contour polygon.  If :obj:`None`,
            ``numpy.finfo(numpy.float64).max`` will be used.

        Returns
        -------
        :
            The result of the :attr:`formatter` called on the filled contour
            between `min` and `max`.

        """
        # pylint: disable=redefined-builtin,redefined-outer-name
        # Get the contour vertices.
        if min is None:
            min = np.finfo(np.float64).min
        if max is None:
            max = np.finfo(np.float64).max
        vertices, codes = (
            self._contour_generator.create_filled_contour(min, max))
        return self.formatter((min, max), vertices, codes)