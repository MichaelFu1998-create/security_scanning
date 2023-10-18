def luminosity_within_ellipse_in_units(self, major_axis : dim.Length, unit_luminosity='eps', kpc_per_arcsec=None, exposure_time=None):
        """Compute the total luminosity of the galaxy's light profiles, within an ellipse of specified major axis. This 
        is performed via integration of each light profile and is centred, oriented and aligned with each light
        model's individual geometry.

        See *light_profiles.luminosity_within_ellipse* for details of how this is performed.

        Parameters
        ----------
        major_axis : float
            The major-axis radius of the ellipse.
        unit_luminosity : str
            The units the luminosity is returned in (eps | counts).
        exposure_time : float
            The exposure time of the observation, which converts luminosity from electrons per second units to counts.
        """
        if self.has_light_profile:
            return sum(map(lambda p: p.luminosity_within_ellipse_in_units(major_axis=major_axis, unit_luminosity=unit_luminosity,
                                                                          kpc_per_arcsec=kpc_per_arcsec, exposure_time=exposure_time),
                           self.light_profiles))
        else:
            return None