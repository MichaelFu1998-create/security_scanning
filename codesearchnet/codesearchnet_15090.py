def is_in_bounds(self, x, y):
        """
        :return: whether ``(x, y)`` is inside the :ref:`bounds
          <png-builder-bounds>`
        :rtype: bool
        """
        lower = self._min_x <= x and self._min_y <= y
        upper = self._max_x > x and self._max_y > y
        return lower and upper