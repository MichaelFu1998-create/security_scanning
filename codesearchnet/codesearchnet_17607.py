def get_element_mass_dictionary(self):
        """
        Determine the masses of elements in the package and return as a
        dictionary.

        :returns: Dictionary of element symbols and masses. [kg]
        """

        element_symbols = self.material.elements
        element_masses = self.get_element_masses()

        return {s: m for s, m in zip(element_symbols, element_masses)}