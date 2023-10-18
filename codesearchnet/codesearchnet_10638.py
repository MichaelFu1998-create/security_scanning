def mass_within_circle_in_units(self, radius, unit_mass='angular', kpc_per_arcsec=None, critical_surface_density=None):
        """Compute the total angular mass of the galaxy's mass profiles within a circle of specified radius.

        See *profiles.mass_profiles.mass_within_circle* for details of how this is performed.

        Parameters
        ----------
        radius : float
            The radius of the circle to compute the dimensionless mass within.
        unit_mass : str
            The units the mass is returned in (angular | solMass).
        critical_surface_density : float
            The critical surface mass density of the strong lens configuration, which converts mass from angulalr \
            units to physical units (e.g. solar masses).
        """
        if self.has_mass_profile:
            return sum(map(lambda p: p.mass_within_circle_in_units(radius=radius, unit_mass=unit_mass,
                                                                   kpc_per_arcsec=kpc_per_arcsec,
                                                                   critical_surface_density=critical_surface_density),
                           self.mass_profiles))
        else:
            return None