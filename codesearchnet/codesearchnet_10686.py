def luminosities_of_galaxies_within_ellipses_in_units(self, major_axis : dim.Length, unit_luminosity='eps',
                                                          exposure_time=None):
        """
        Compute the total luminosity of all galaxies in this plane within a ellipse of specified major-axis.

        The value returned by this integral is dimensionless, and a conversion factor can be specified to convert it \
        to a physical value (e.g. the photometric zeropoint).

        See *galaxy.light_within_ellipse* and *light_profiles.light_within_ellipse* for details
        of how this is performed.

        Parameters
        ----------
        major_axis : float
            The major-axis radius of the ellipse.
        units_luminosity : str
            The units the luminosity is returned in (eps | counts).
        exposure_time : float
            The exposure time of the observation, which converts luminosity from electrons per second units to counts.
        """
        return list(map(lambda galaxy: galaxy.luminosity_within_ellipse_in_units(
            major_axis=major_axis, unit_luminosity=unit_luminosity, kpc_per_arcsec=self.kpc_per_arcsec,
            exposure_time=exposure_time),
                        self.galaxies))