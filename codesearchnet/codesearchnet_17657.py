def create_package(self, assay=None, mass=0.0, normalise=True):
        """
        Create a MaterialPackage based on the specified parameters.

        :param assay: The name of the assay based on which the package must be
          created.
        :param mass: [kg] The mass of the package.
        :param normalise: Indicates whether the assay must be normalised before
          creating the package.

        :returns: The created MaterialPackage.
        """

        if assay is None:
            return MaterialPackage(self, self.create_empty_assay())

        if normalise:
            assay_total = self.get_assay_total(assay)
        else:
            assay_total = 1.0
        return MaterialPackage(self, mass * self.assays[assay] / assay_total)