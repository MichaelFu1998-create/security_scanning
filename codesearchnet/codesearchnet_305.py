def clip_out_of_image(self):
        """
        Clip off all parts of the line strings that are outside of the image.

        Returns
        -------
        imgaug.augmentables.lines.LineStringsOnImage
            Line strings, clipped to fall within the image dimensions.

        """
        lss_cut = [ls_clipped
                   for ls in self.line_strings
                   for ls_clipped in ls.clip_out_of_image(self.shape)]
        return LineStringsOnImage(lss_cut, shape=self.shape)