def normalized_distance(self, image):
        """Calculates the distance of a given image to the
        original image.

        Parameters
        ----------
        image : `numpy.ndarray`
            The image that should be compared to the original image.

        Returns
        -------
        :class:`Distance`
            The distance between the given image and the original image.

        """
        return self.__distance(
            self.__original_image_for_distance,
            image,
            bounds=self.bounds())