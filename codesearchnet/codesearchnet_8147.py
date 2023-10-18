def set_color_list(self, color_list, offset=0):
        """
        Set the internal colors starting at an optional offset.

        If `color_list` is a list or other 1-dimensional array, it is reshaped
        into an N x 3 list.

        If `color_list` too long it is truncated; if it is too short then only
        the initial colors are set.
        """
        if not len(color_list):
            return
        color_list = make.colors(color_list)

        size = len(self._colors) - offset
        if len(color_list) > size:
            color_list = color_list[:size]
        self._colors[offset:offset + len(color_list)] = color_list