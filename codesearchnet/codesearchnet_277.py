def is_out_of_image(self, image, fully=True, partly=False, default=True):
        """
        Estimate whether the line is partially/fully outside of the image area.

        Parameters
        ----------
        image : ndarray or tuple of int
            Either an image with shape ``(H,W,[C])`` or a tuple denoting
            such an image shape.

        fully : bool, optional
            Whether to return True if the bounding box is fully outside fo the
            image area.

        partly : bool, optional
            Whether to return True if the bounding box is at least partially
            outside fo the image area.

        default
            Default value to return if the line string contains no points.

        Returns
        -------
        bool
            `default` if the line string has no points.
            True if the line string is partially/fully outside of the image
            area, depending on defined parameters.
            False otherwise.

        """
        if len(self.coords) == 0:
            return default

        if self.is_fully_within_image(image):
            return False
        elif self.is_partly_within_image(image):
            return partly
        else:
            return fully