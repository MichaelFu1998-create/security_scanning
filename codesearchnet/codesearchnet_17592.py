def create_package(self, assay=None, mass=0.0, P=1.0, T=25.0,
                       normalise=True):
        """
        Create a MaterialPackage based on the specified parameters.

        :param assay:     Name of the assay to be used to create the package.
        :param mass:      Package mass. [kg]
        :param P:         Package pressure. [atm]
        :param T:         Package temperature. [°C]
        :param normalise: Indicates whether the assay must be normalised
          before creating the package.

        :returns: MaterialPackage object.
        """

        if assay is None:
            return MaterialPackage(self, self.create_empty_assay(), P, T)

        if normalise:
            assay_total = self.get_assay_total(assay)
        else:
            assay_total = 1.0

        return MaterialPackage(self, mass * self.converted_assays[assay] /
                               assay_total, P, T, self._isCoal(assay),
                               self._get_HHV(assay))