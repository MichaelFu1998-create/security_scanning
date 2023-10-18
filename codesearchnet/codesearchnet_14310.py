def breaks(self, limits):
        """
        Calculate breaks in data space and return them
        in transformed space.

        Expects limits to be in *transform space*, this
        is the same space as that where the domain is
        specified.

        This method wraps around :meth:`breaks_` to ensure
        that the calculated breaks are within the domain
        the transform. This is helpful in cases where an
        aesthetic requests breaks with limits expanded for
        some padding, yet the expansion goes beyond the
        domain of the transform. e.g for a probability
        transform the breaks will be in the domain
        ``[0, 1]`` despite any outward limits.

        Parameters
        ----------
        limits : tuple
            The scale limits. Size 2.

        Returns
        -------
        out : array_like
            Major breaks
        """
        # clip the breaks to the domain,
        # e.g. probabilities will be in [0, 1] domain
        vmin = np.max([self.domain[0], limits[0]])
        vmax = np.min([self.domain[1], limits[1]])
        breaks = np.asarray(self.breaks_([vmin, vmax]))

        # Some methods(mpl_breaks, extended_breaks) that
        # calculate breaks take the limits as guide posts and
        # not hard limits.
        breaks = breaks.compress((breaks >= self.domain[0]) &
                                 (breaks <= self.domain[1]))
        return breaks