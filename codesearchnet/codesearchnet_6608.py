def y_offset(self):
        """
        :return: The Y offset of the data in the buffer in number of pixels from the image origin to handle areas of interest.
        """
        try:
            if self._part:
                value = self._part.y_offset
            else:
                value = self._buffer.offset_y
        except InvalidParameterException:
            value = self._node_map.OffsetY.value
        return value