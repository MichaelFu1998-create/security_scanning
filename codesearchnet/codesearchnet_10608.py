def mass_within_ellipse_in_units(self, major_axis, unit_mass='angular', kpc_per_arcsec=None,
                                     critical_surface_density=None):
        """ Integrate the mass profiles's convergence profile to compute the total angular mass within an ellipse of \
        specified major axis. This is centred on the mass profile.

        The following units for mass can be specified and output:

        - Dimensionless angular units (default) - 'angular'.
        - Solar masses - 'angular' (multiplies the angular mass by the critical surface mass density)

        Parameters
        ----------
        major_axis : float
            The major-axis radius of the ellipse.
        unit_mass : str
            The units the mass is returned in (angular | angular).
        critical_surface_density : float or None
            The critical surface mass density of the strong lens configuration, which converts mass from angular \
            units to phsical units (e.g. solar masses).
        """

        self.check_units_of_radius_and_critical_surface_density(
            radius=major_axis, critical_surface_density=critical_surface_density)

        profile = self.new_profile_with_units_converted(
            unit_length=major_axis.unit_length, unit_mass='angular',
            kpc_per_arcsec=kpc_per_arcsec, critical_surface_density=critical_surface_density)

        mass_angular = dim.Mass(value=quad(profile.mass_integral, a=0.0, b=major_axis, args=(self.axis_ratio,))[0],
                                unit_mass='angular')
        return mass_angular.convert(unit_mass=unit_mass, critical_surface_density=critical_surface_density)