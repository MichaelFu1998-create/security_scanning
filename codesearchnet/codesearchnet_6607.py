def x_offset(self):  # TODO: Check the naming convention.
        """
        :return: The X offset of the data in the buffer in number of pixels from the image origin to handle areas of interest.
        """
        try:
            if self._part:
                value = self._part.x_offset
            else:
                value = self._buffer.offset_x
        except InvalidParameterException:
            value = self._node_map.OffsetX.value
        return value