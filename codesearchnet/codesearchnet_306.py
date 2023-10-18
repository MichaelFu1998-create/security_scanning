def shift(self, top=None, right=None, bottom=None, left=None):
        """
        Shift/move the line strings from one or more image sides.

        Parameters
        ----------
        top : None or int, optional
            Amount of pixels by which to shift all bounding boxes from the
            top.

        right : None or int, optional
            Amount of pixels by which to shift all bounding boxes from the
            right.

        bottom : None or int, optional
            Amount of pixels by which to shift all bounding boxes from the
            bottom.

        left : None or int, optional
            Amount of pixels by which to shift all bounding boxes from the
            left.

        Returns
        -------
        imgaug.augmentables.lines.LineStringsOnImage
            Shifted line strings.

        """
        lss_new = [ls.shift(top=top, right=right, bottom=bottom, left=left)
                   for ls in self.line_strings]
        return LineStringsOnImage(lss_new, shape=self.shape)