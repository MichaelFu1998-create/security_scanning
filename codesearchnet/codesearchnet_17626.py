def get_element_mfr(self, element):
        """
        Determine the mass flow rate of the specified elements in the stream.

        :returns: Mass flow rates. [kg/h]
        """

        result = 0.0
        for compound in self.material.compounds:
            formula = compound.split('[')[0]
            result += self.get_compound_mfr(compound) *\
                stoich.element_mass_fraction(formula, element)
        return result