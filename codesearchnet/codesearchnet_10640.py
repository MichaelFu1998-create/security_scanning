def einstein_radius_in_units(self, unit_length='arcsec', kpc_per_arcsec=None):
        """The Einstein Radius of this galaxy, which is the sum of Einstein Radii of its mass profiles.

        If the galaxy is composed of multiple ellipitcal profiles with different axis-ratios, this Einstein Radius \
        may be inaccurate. This is because the differently oriented ellipses of each mass profile """

        if self.has_mass_profile:
            return sum(map(lambda p: p.einstein_radius_in_units(unit_length=unit_length, kpc_per_arcsec=kpc_per_arcsec),
                           self.mass_profiles))
        else:
            return None