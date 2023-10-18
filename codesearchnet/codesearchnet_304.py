def remove_out_of_image(self, fully=True, partly=False):
        """
        Remove all line strings that are fully/partially outside of the image.

        Parameters
        ----------
        fully : bool, optional
            Whether to remove line strings that are fully outside of the image.

        partly : bool, optional
            Whether to remove line strings that are partially outside of the
            image.

        Returns
        -------
        imgaug.augmentables.lines.LineStringsOnImage
            Reduced set of line strings, with those that were fully/partially
            outside of the image removed.

        """
        lss_clean = [ls for ls in self.line_strings
                     if not ls.is_out_of_image(
                         self.shape, fully=fully, partly=partly)]
        return LineStringsOnImage(lss_clean, shape=self.shape)