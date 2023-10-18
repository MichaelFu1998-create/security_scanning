def get_element_masses(self):
        """
        Get the masses of elements in the package.

        :returns: [kg] An array of element masses. The sequence of the elements
          in the result corresponds with the sequence of elements in the
          element list of the material.
        """

        result = [0] * len(self.material.elements)
        for compound in self.material.compounds:
            c = self.get_compound_mass(compound)
            f = [c * x for x in emf(compound, self.material.elements)]
            result = [v+f[ix] for ix, v in enumerate(result)]

        return result