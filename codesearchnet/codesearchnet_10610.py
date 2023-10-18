def density_between_circular_annuli_in_angular_units(self, inner_annuli_radius, outer_annuli_radius):
        """Calculate the mass between two circular annuli and compute the density by dividing by the annuli surface
        area.

        The value returned by the mass integral is dimensionless, therefore the density between annuli is returned in \
        units of inverse radius squared. A conversion factor can be specified to convert this to a physical value \
        (e.g. the critical surface mass density).

        Parameters
        -----------
        inner_annuli_radius : float
            The radius of the inner annulus outside of which the density are estimated.
        outer_annuli_radius : float
            The radius of the outer annulus inside of which the density is estimated.
        """
        annuli_area = (np.pi * outer_annuli_radius ** 2.0) - (np.pi * inner_annuli_radius ** 2.0)
        return (self.mass_within_circle_in_units(radius=outer_annuli_radius) -
                self.mass_within_circle_in_units(radius=inner_annuli_radius)) \
               / annuli_area