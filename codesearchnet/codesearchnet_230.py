def shift(self, top=None, right=None, bottom=None, left=None):
        """
        Shift all polygons from one or more image sides, i.e. move them on the x/y-axis.

        Parameters
        ----------
        top : None or int, optional
            Amount of pixels by which to shift all polygons from the top.

        right : None or int, optional
            Amount of pixels by which to shift all polygons from the right.

        bottom : None or int, optional
            Amount of pixels by which to shift all polygons from the bottom.

        left : None or int, optional
            Amount of pixels by which to shift all polygons from the left.

        Returns
        -------
        imgaug.PolygonsOnImage
            Shifted polygons.

        """
        polys_new = [
            poly.shift(top=top, right=right, bottom=bottom, left=left)
            for poly
            in self.polygons
        ]
        return PolygonsOnImage(polys_new, shape=self.shape)