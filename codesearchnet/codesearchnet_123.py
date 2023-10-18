def is_partly_within_image(self, image):
        """
        Estimate whether the bounding box is at least partially inside the image area.

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
            True if the bounding box is at least partially inside the image area. False otherwise.

        """
        shape = normalize_shape(image)
        height, width = shape[0:2]
        eps = np.finfo(np.float32).eps
        img_bb = BoundingBox(x1=0, x2=width-eps, y1=0, y2=height-eps)
        return self.intersection(img_bb) is not None