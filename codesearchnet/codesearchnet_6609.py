def x_padding(self):
        """
        Returns
        :return: The X padding of the data component in the buffer in number of pixels.
        """
        try:
            if self._part:
                value = self._part.x_padding
            else:
                value = self._buffer.padding_x
        except InvalidParameterException:
            value = 0
        return value