def is_partly_within_image(self, image, default=False):
        """
        Estimate whether the line string is at least partially inside the image.

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
            True if the line string is at least partially inside the image area.
            False otherwise.

        """
        if len(self.coords) == 0:
            return default
        # check mask first to avoid costly computation of intersection points
        # whenever possible
        mask = self.get_pointwise_inside_image_mask(image)
        if np.any(mask):
            return True
        return len(self.clip_out_of_image(image)) > 0