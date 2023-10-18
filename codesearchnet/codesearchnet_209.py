def is_out_of_image(self, image, fully=True, partly=False):
        """
        Estimate whether the polygon is partially or fully outside of the image area.

        Parameters
        ----------
        image : (H,W,...) ndarray or tuple of int
            Image dimensions to use.
            If an ndarray, its shape will be used.
            If a tuple, it is assumed to represent the image shape and must contain at least two integers.

        fully : bool, optional
            Whether to return True if the polygon is fully outside of the image area.

        partly : bool, optional
            Whether to return True if the polygon is at least partially outside fo the image area.

        Returns
        -------
        bool
            True if the polygon is partially/fully outside of the image area, depending
            on defined parameters. False otherwise.

        """
        # TODO this is inconsistent with line strings, which return a default
        #      value in these cases
        if len(self.exterior) == 0:
            raise Exception("Cannot determine whether the polygon is inside the image, because it contains no points.")
        ls = self.to_line_string()
        return ls.is_out_of_image(image, fully=fully, partly=partly)