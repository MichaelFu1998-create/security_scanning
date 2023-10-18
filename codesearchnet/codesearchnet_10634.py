def luminosity_within_circle_in_units(self, radius : dim.Length, unit_luminosity='eps', kpc_per_arcsec=None, exposure_time=None):
        """Compute the total luminosity of the galaxy's light profiles within a circle of specified radius.

        See *light_profiles.luminosity_within_circle* for details of how this is performed.

        Parameters
        ----------
        radius : float
            The radius of the circle to compute the dimensionless mass within.
        unit_luminosity : str
            The units the luminosity is returned in (eps | counts).
        exposure_time : float
            The exposure time of the observation, which converts luminosity from electrons per second units to counts.
        """
        if self.has_light_profile:
            return sum(map(lambda p: p.luminosity_within_circle_in_units(radius=radius, unit_luminosity=unit_luminosity,
                                                                         kpc_per_arcsec=kpc_per_arcsec, exposure_time=exposure_time),
                           self.light_profiles))
        else:
            return None