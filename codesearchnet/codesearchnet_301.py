def from_xy_arrays(cls, xy, shape):
        """
        Convert an `(N,M,2)` ndarray to a LineStringsOnImage object.

        This is the inverse of
        :func:`imgaug.augmentables.lines.LineStringsOnImage.to_xy_array`.

        Parameters
        ----------
        xy : (N,M,2) ndarray or iterable of (M,2) ndarray
            Array containing the point coordinates ``N`` line strings
            with each ``M`` points given as ``(x,y)`` coordinates.
            ``M`` may differ if an iterable of arrays is used.
            Each array should usually be of dtype ``float32``.

        shape : tuple of int
            ``(H,W,[C])`` shape of the image on which the line strings are
            placed.

        Returns
        -------
        imgaug.augmentables.lines.LineStringsOnImage
            Object containing a list of ``LineString`` objects following the
            provided point coordinates.

        """
        lss = []
        for xy_ls in xy:
            lss.append(LineString(xy_ls))
        return cls(lss, shape)