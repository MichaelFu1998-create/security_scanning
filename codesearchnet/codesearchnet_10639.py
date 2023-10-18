def mass_within_ellipse_in_units(self, major_axis, unit_mass='angular', kpc_per_arcsec=None, critical_surface_density=None):
        """Compute the total angular mass of the galaxy's mass profiles within an ellipse of specified major_axis.

        See *profiles.mass_profiles.angualr_mass_within_ellipse* for details of how this is performed.

        Parameters
        ----------
        major_axis : float
            The major-axis radius of the ellipse.
        units_luminosity : str
            The units the luminosity is returned in (eps | counts).
        exposure_time : float
            The exposure time of the observation, which converts luminosity from electrons per second units to counts.
        """
        if self.has_mass_profile:
            return sum(map(lambda p: p.mass_within_ellipse_in_units(major_axis=major_axis, unit_mass=unit_mass,
                                                                    kpc_per_arcsec=kpc_per_arcsec,
                                                                    critical_surface_density=critical_surface_density),
                           self.mass_profiles))
        else:
            return None