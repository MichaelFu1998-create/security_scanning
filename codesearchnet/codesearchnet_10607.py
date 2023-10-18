def mass_within_circle_in_units(self, radius: dim.Length, unit_mass='angular', kpc_per_arcsec=None,
                                    critical_surface_density=None):
        """ Integrate the mass profiles's convergence profile to compute the total mass within a circle of \
        specified radius. This is centred on the mass profile.

        The following units for mass can be specified and output:

        - Dimensionless angular units (default) - 'angular'.
        - Solar masses - 'angular' (multiplies the angular mass by the critical surface mass density).

        Parameters
        ----------
        radius : dim.Length
            The radius of the circle to compute the dimensionless mass within.
        unit_mass : str
            The units the mass is returned in (angular | angular).
        critical_surface_density : float or None
            The critical surface mass density of the strong lens configuration, which converts mass from angulalr \
            units to phsical units (e.g. solar masses).
        """

        self.check_units_of_radius_and_critical_surface_density(
            radius=radius, critical_surface_density=critical_surface_density)

        profile = self.new_profile_with_units_converted(
            unit_length=radius.unit_length, unit_mass='angular',
            kpc_per_arcsec=kpc_per_arcsec, critical_surface_density=critical_surface_density)

        mass_angular = dim.Mass(value=quad(profile.mass_integral, a=0.0, b=radius, args=(1.0,))[0], unit_mass='angular')
        return mass_angular.convert(unit_mass=unit_mass, critical_surface_density=critical_surface_density)