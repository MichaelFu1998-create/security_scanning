def add_to(self, other):
        """
        Add another psd material package to this material package.

        :param other: The other material package.
        """

        # Add another package.
        if type(other) is MaterialPackage:
            # Packages of the same material.
            if self.material == other.material:
                self.size_class_masses = \
                        self.size_class_masses + other.size_class_masses
            else:  # Packages of different materials.
                for size_class in other.material.size_classes:
                    if size_class not in self.material.size_classes:
                        raise Exception(
                            "Packages of '" + other.material.name +
                            "' cannot be added to packages of '" +
                            self.material.name +
                            "'. The size class '" + size_class +
                            "' was not found in '" + self.material.name + "'.")
                    self.add_to(
                        (size_class, other.get_size_class_mass(size_class)))

        # Add the specified mass of the specified size class.
        elif self._is_size_class_mass_tuple(other):
            # Added material variables.
            size_class = other[0]
            compound_index = self.material.get_size_class_index(size_class)
            mass = other[1]

            # Create the result package.
            self.size_class_masses[compound_index] = \
                self.size_class_masses[compound_index] + mass

        # If not one of the above, it must be an invalid argument.
        else:
            raise TypeError("Invalid addition argument.")