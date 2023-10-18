def create_package(self, assay=None, mass=0.0, normalise=True):
        """
        Create a MaterialPackage based on the specified parameters.

        :param assay: The name of the assay based on which the package
          must be created.
        :param mass: [kg] The mass of the package.
        :param normalise: Indicates whether the assay must be normalised
          before creating the package.

        :returns: The created MaterialPackage.
        """

        if assay is None:
            return MaterialPackage(self, 1.0, 0.0, self.create_empty_assay())

        if normalise:
            assay_total = self.get_assay_total(assay)
            if assay_total == 0.0:
                assay_total = 1.0
        else:
            assay_total = 1.0
        H2O_mass = mass * self.H2O_fractions[assay]
        solid_mass = mass - H2O_mass
        return MaterialPackage(self,
                               self.solid_densities[assay],
                               H2O_mass,
                               solid_mass * self.assays[assay] / assay_total)