def to_xy_arrays(self, dtype=np.float32):
        """
        Convert this object to an iterable of ``(M,2)`` arrays of points.

        This is the inverse of
        :func:`imgaug.augmentables.lines.LineStringsOnImage.from_xy_array`.

        Parameters
        ----------
        dtype : numpy.dtype, optional
            Desired output datatype of the ndarray.

        Returns
        -------
        list of ndarray
            The arrays of point coordinates, each given as ``(M,2)``.

        """
        from .. import dtypes as iadt
        return [iadt.restore_dtypes_(np.copy(ls.coords), dtype)
                for ls in self.line_strings]