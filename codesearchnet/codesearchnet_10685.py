def luminosities_of_galaxies_within_circles_in_units(self, radius : dim.Length, unit_luminosity='eps', exposure_time=None):
        """Compute the total luminosity of all galaxies in this plane within a circle of specified radius.

        See *galaxy.light_within_circle* and *light_profiles.light_within_circle* for details \
        of how this is performed.

        Parameters
        ----------
        radius : float
            The radius of the circle to compute the dimensionless mass within.
        units_luminosity : str
            The units the luminosity is returned in (eps | counts).
        exposure_time : float
            The exposure time of the observation, which converts luminosity from electrons per second units to counts.
        """
        return list(map(lambda galaxy: galaxy.luminosity_within_circle_in_units(
            radius=radius, unit_luminosity=unit_luminosity, kpc_per_arcsec=self.kpc_per_arcsec,
            exposure_time=exposure_time),
                        self.galaxies))