def delivered_image_height(self):
        """
        :return: The image height of the data component.
        """
        try:
            if self._part:
                value = self._part.delivered_image_height
            else:
                value = self._buffer.delivered_image_height
        except InvalidParameterException:
            value = 0
        return value