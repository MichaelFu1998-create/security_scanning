def get_element_mfrs(self, elements=None):
        """
        Determine the mass flow rates of elements in the stream.

        :returns: Array of element mass flow rates. [kg/h]
        """

        if elements is None:
            elements = self.material.elements
        result = numpy.zeros(len(elements))
        for compound in self.material.compounds:
            result += self.get_compound_mfr(compound) *\
                stoich.element_mass_fractions(compound, elements)
        return result