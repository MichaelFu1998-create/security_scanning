def bounding_box(self):
        """The minimum and maximum bounds of this layout.

        :return: ``(min_x, min_y, max_x, max_y)`` the bounding box
          of this layout
        :rtype: tuple
        """
        min_x, min_y, max_x, max_y = zip(*list(self.walk_rows(
            lambda row: row.bounding_box)))
        return min(min_x), min(min_y), max(max_x), max(max_y)