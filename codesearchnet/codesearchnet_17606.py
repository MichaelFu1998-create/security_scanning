def get_element_masses(self, elements=None):
        """
        Determine the masses of elements in the package.

        :returns: Array of element masses. [kg]
        """

        if elements is None:
            elements = self.material.elements
        result = numpy.zeros(len(elements))

        for compound in self.material.compounds:
            result += self.get_compound_mass(compound) *\
                numpy.array(stoich.element_mass_fractions(compound, elements))
        return result