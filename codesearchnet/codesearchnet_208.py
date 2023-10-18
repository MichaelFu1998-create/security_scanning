def is_partly_within_image(self, image):
        """
        Estimate whether the polygon is at least partially inside the image area.

        Parameters
        ----------
        image : (H,W,...) ndarray or tuple of int
            Image dimensions to use.
            If an ndarray, its shape will be used.
            If a tuple, it is assumed to represent the image shape and must contain at least two integers.

        Returns
        -------
        bool
            True if the polygon is at least partially inside the image area.
            False otherwise.

        """
        return not self.is_out_of_image(image, fully=True, partly=False)