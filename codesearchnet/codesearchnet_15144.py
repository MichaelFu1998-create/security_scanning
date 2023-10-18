def bounding_box(self):
        """the bounding box of this SVG
        ``(min_x, min_y, max_x, max_y)``.

        .. code:: python

            svg_builder10x10.bounding_box = (0, 0, 10, 10)
            assert svg_builder10x10.bounding_box == (0, 0, 10, 10)

        ``viewBox``, ``width`` and ``height`` are computed from this.

        If the bounding box was never set, the result is a tuple of four
        :obj:`None`.
        """
        return (self._min_x, self._min_y, self._max_x, self._max_y)