def masses_of_galaxies_within_circles_in_units(self, radius : dim.Length, unit_mass='angular',
                                                   critical_surface_density=None):
        """Compute the total mass of all galaxies in this plane within a circle of specified radius.

        See *galaxy.angular_mass_within_circle* and *mass_profiles.angular_mass_within_circle* for details
        of how this is performed.

        Parameters
        ----------
        radius : float
            The radius of the circle to compute the dimensionless mass within.
        units_mass : str
            The units the mass is returned in (angular | solMass).
        critical_surface_density : float
            The critical surface mass density of the strong lens configuration, which converts mass from angulalr \
            units to physical units (e.g. solar masses).
        """
        return list(map(lambda galaxy: galaxy.mass_within_circle_in_units(
                        radius=radius, unit_mass=unit_mass, kpc_per_arcsec=self.kpc_per_arcsec,
                        critical_surface_density=critical_surface_density),
                        self.galaxies))