def is_out_of_image(self, image, fully=True, partly=False):
        """
        Estimate whether the bounding box is partially or fully outside of the image area.

        Parameters
        ----------
        image : (H,W,...) ndarray or tuple of int
            Image dimensions to use. If an ndarray, its shape will be used. If a tuple, it is
            assumed to represent the image shape and must contain at least two integers.

        fully : bool, optional
            Whether to return True if the bounding box is fully outside fo the image area.

        partly : bool, optional
            Whether to return True if the bounding box is at least partially outside fo the
            image area.

        Returns
        -------
        bool
            True if the bounding box is partially/fully outside of the image area, depending
            on defined parameters. False otherwise.

        """
        if self.is_fully_within_image(image):
            return False
        elif self.is_partly_within_image(image):
            return partly
        else:
            return fully