def width(self):
        """
        :return: The width of the data component in the buffer in number of pixels.
        """
        try:
            if self._part:
                value = self._part.width
            else:
                value = self._buffer.width
        except InvalidParameterException:
            value = self._node_map.Width.value
        return value