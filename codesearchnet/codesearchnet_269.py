def get_pointwise_inside_image_mask(self, image):
        """
        Get for each point whether it is inside of the given image plane.

        Parameters
        ----------
        image : ndarray or tuple of int
            Either an image with shape ``(H,W,[C])`` or a tuple denoting
            such an image shape.

        Returns
        -------
        ndarray
            Boolean array with one value per point indicating whether it is
            inside of the provided image plane (``True``) or not (``False``).

        """
        if len(self.coords) == 0:
            return np.zeros((0,), dtype=bool)
        shape = normalize_shape(image)
        height, width = shape[0:2]
        x_within = np.logical_and(0 <= self.xx, self.xx < width)
        y_within = np.logical_and(0 <= self.yy, self.yy < height)
        return np.logical_and(x_within, y_within)