def scale(self, factor, center=None):
        """Resize the shape by a proportion (e.g., 1 is unchanged), in-place.

        Parameters
        ----------
        factor : float or array-like
            If a scalar, the same factor will be applied in the x and y dimensions.
        center : array-like, optional
            Point around which to perform the scaling.
            If not passed, the center of the shape is used.

        """
        factor = np.asarray(factor)

        if len(factor.shape):
            args = list(factor)
        else:
            args = [factor, factor]
        if center is not None:
            args.extend(center)

        self.poly.scale(*args)
        return self