def get_element_mass(self, element):
        """
        Determine the masses of elements in the package.

        :returns: [kg] An array of element masses. The sequence of the elements
          in the result corresponds with the sequence of elements in the
          element list of the material.
        """

        result = [0]
        for compound in self.material.compounds:
            c = self.get_compound_mass(compound)
            f = [c * x for x in emf(compound, [element])]
            result = [v+f[ix] for ix, v in enumerate(result)]

        return result[0]