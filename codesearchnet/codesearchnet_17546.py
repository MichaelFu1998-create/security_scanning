def add_to(self, other):
        """
        Add another chem material package to this material package.

        :param other: The other material package.
        """

        # Add another package.
        if type(other) is MaterialPackage:

            # Packages of the same material.
            if self.material == other.material:
                self.compound_masses += other.compound_masses

            # Packages of different materials.
            else:
                for compound in other.material.compounds:
                    if compound not in self.material.compounds:
                        raise Exception("Packages of '" + other.material.name +
                                        "' cannot be added to packages of '" +
                                        self.material.name +
                                        "'. The compound '" + compound +
                                        "' was not found in '" +
                                        self.material.name + "'.")
                    self.add_to((compound, other.get_compound_mass(compound)))

        # Add the specified mass of the specified compound.
        elif self._is_compound_mass_tuple(other):
            # Added material variables.
            compound = other[0]
            compound_index = self.material.get_compound_index(compound)
            mass = other[1]

            # Create the result package.
            self.compound_masses[compound_index] += mass

        # If not one of the above, it must be an invalid argument.
        else:
            raise TypeError('Invalid addition argument.')