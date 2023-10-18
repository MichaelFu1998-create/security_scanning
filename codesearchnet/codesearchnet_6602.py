def represent_pixel_location(self):
        """
        Returns a NumPy array that represents the 2D pixel location,
        which is defined by PFNC, of the original image data.

        You may use the returned NumPy array for a calculation to map the
        original image to another format.

        :return: A NumPy array that represents the 2D pixel location.
        """
        if self.data is None:
            return None

        #
        return self._data.reshape(
            self.height + self.y_padding,
            int(self.width * self._num_components_per_pixel + self.x_padding)
        )