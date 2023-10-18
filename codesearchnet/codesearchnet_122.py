def is_fully_within_image(self, image):
        """
        Estimate whether the bounding box is fully inside the image area.

        Parameters
        ----------
        image : (H,W,...) ndarray or tuple of int
            Image dimensions to use.
            If an ndarray, its shape will be used.
            If a tuple, it is assumed to represent the image shape
            and must contain at least two integers.

        Returns
        -------
        bool
            True if the bounding box is fully inside the image area. False otherwise.

        """
        shape = normalize_shape(image)
        height, width = shape[0:2]
        return self.x1 >= 0 and self.x2 < width and self.y1 >= 0 and self.y2 < height