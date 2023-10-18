def height(self):
        """
        :return: The height of the data component in the buffer in number of pixels.
        """
        try:
            if self._part:
                value = self._part.height
            else:
                value = self._buffer.height
        except InvalidParameterException:
            value = self._node_map.Height.value
        return value