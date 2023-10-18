def clip_out_of_image(self, image):
        """
        Clip off all parts of the bounding box that are outside of the image.

        Parameters
        ----------
        image : (H,W,...) ndarray or tuple of int
            Image dimensions to use for the clipping of the bounding box.
            If an ndarray, its shape will be used.
            If a tuple, it is assumed to represent the image shape and must contain at least two integers.

        Returns
        -------
        result : imgaug.BoundingBox
            Bounding box, clipped to fall within the image dimensions.

        """
        shape = normalize_shape(image)

        height, width = shape[0:2]
        ia.do_assert(height > 0)
        ia.do_assert(width > 0)

        eps = np.finfo(np.float32).eps
        x1 = np.clip(self.x1, 0, width - eps)
        x2 = np.clip(self.x2, 0, width - eps)
        y1 = np.clip(self.y1, 0, height - eps)
        y2 = np.clip(self.y2, 0, height - eps)

        return self.copy(
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2,
            label=self.label
        )