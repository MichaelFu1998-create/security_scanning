def set_colors(self, colors, pos):
        """
        Use with caution!

        Directly set the pixel buffers.

        :param colors: A list of color tuples
        :param int pos: Position in color list to begin set operation.
        """
        self._colors = colors
        self._pos = pos

        end = self._pos + self.numLEDs
        if end > len(self._colors):
            raise ValueError('Needed %d colors but found %d' % (
                end, len(self._colors)))