def data_format_value(self):
        """
        :return: The data type of the data component as integer value.
        """
        try:
            if self._part:
                value = self._part.data_format
            else:
                value = self._buffer.pixel_format
        except InvalidParameterException:
            value = self._node_map.PixelFormat.value
        return value