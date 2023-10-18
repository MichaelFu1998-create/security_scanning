def shift(self, top=None, right=None, bottom=None, left=None):
        """
        Shift the polygon from one or more image sides, i.e. move it on the x/y-axis.

        Parameters
        ----------
        top : None or int, optional
            Amount of pixels by which to shift the polygon from the top.

        right : None or int, optional
            Amount of pixels by which to shift the polygon from the right.

        bottom : None or int, optional
            Amount of pixels by which to shift the polygon from the bottom.

        left : None or int, optional
            Amount of pixels by which to shift the polygon from the left.

        Returns
        -------
        imgaug.Polygon
            Shifted polygon.

        """
        ls_shifted = self.to_line_string(closed=False).shift(
            top=top, right=right, bottom=bottom, left=left)
        return self.copy(exterior=ls_shifted.coords)