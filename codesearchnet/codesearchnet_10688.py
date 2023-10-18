def masses_of_galaxies_within_ellipses_in_units(self, major_axis : dim.Length, unit_mass='angular',
                                                    critical_surface_density=None):
        """Compute the total mass of all galaxies in this plane within a ellipse of specified major-axis.

        See *galaxy.angular_mass_within_ellipse* and *mass_profiles.angular_mass_within_ellipse* for details \
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
        return list(map(lambda galaxy: galaxy.mass_within_ellipse_in_units(
                        major_axis=major_axis, unit_mass=unit_mass, kpc_per_arcsec=self.kpc_per_arcsec,
                        critical_surface_density=critical_surface_density),
                        self.galaxies))