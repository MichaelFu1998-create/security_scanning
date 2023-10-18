def average_convergence_of_1_radius_in_units(self, unit_length='arcsec', kpc_per_arcsec=None):
        """The radius a critical curve forms for this mass profile, e.g. where the mean convergence is equal to 1.0.

         In case of ellipitical mass profiles, the 'average' critical curve is used, whereby the convergence is \
         rescaled into a circle using the axis ratio.

         This radius corresponds to the Einstein radius of the mass profile, and is a property of a number of \
         mass profiles below.
         """

        def func(radius):
            radius = dim.Length(radius, unit_length=unit_length)
            return self.mass_within_circle_in_units(radius=radius) - np.pi * radius ** 2.0

        radius = self.ellipticity_rescale * root_scalar(func, bracket=[1e-4, 1000.0]).root
        radius = dim.Length(radius, unit_length)
        return radius.convert(unit_length=unit_length, kpc_per_arcsec=kpc_per_arcsec)