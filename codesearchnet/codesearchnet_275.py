def is_fully_within_image(self, image, default=False):
        """
        Estimate whether the line string is fully inside the image area.

        Parameters
        ----------
        image : ndarray or tuple of int
            Either an image with shape ``(H,W,[C])`` or a tuple denoting
            such an image shape.

        default
            Default value to return if the line string contains no points.

        Returns
        -------
        bool
            True if the line string is fully inside the image area.
            False otherwise.

        """
        if len(self.coords) == 0:
            return default
        return np.all(self.get_pointwise_inside_image_mask(image))