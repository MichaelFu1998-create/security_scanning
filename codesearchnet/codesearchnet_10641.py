def einstein_mass_in_units(self, unit_mass='angular', critical_surface_density=None):
        """The Einstein Mass of this galaxy, which is the sum of Einstein Radii of its mass profiles.

        If the galaxy is composed of multiple ellipitcal profiles with different axis-ratios, this Einstein Mass \
        may be inaccurate. This is because the differently oriented ellipses of each mass profile """

        if self.has_mass_profile:
            return sum(
                map(lambda p: p.einstein_mass_in_units(unit_mass=unit_mass,
                                                       critical_surface_density=critical_surface_density),
                    self.mass_profiles))
        else:
            return None