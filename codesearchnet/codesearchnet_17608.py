def get_element_mass(self, element):
        """
        Determine the mass of the specified elements in the package.

        :returns: Masses. [kg]
        """

        result = numpy.zeros(1)
        for compound in self.material.compounds:
            result += self.get_compound_mass(compound) *\
                numpy.array(stoich.element_mass_fractions(compound, [element]))
        return result[0]