def extract(self, other):
        """
        Extract 'other' from self, modifying self and returning the extracted
        material as a new package.

        :param other: Can be one of the following:

          * float: A mass equal to other is extracted from self. Self is
            reduced by other and the extracted package is returned as a new
            package.
          * tuple (size class, mass): The other tuple specifies the mass
            of a size class to be extracted. It is extracted from self and
            the extracted mass is returned as a new package.
          * string: The 'other' string specifies the size class to be
            extracted. All of the mass of that size class will be removed
            from self and a new package created with it.


        :returns: A new material package containing the material that was
          extracted from self.
        """

        # Extract the specified mass.
        if type(other) is float or \
                type(other) is numpy.float64 or \
                type(other) is numpy.float32:
            if other > self.get_mass():
                raise Exception(
                    "Invalid extraction operation. "
                    "Cannot extract a mass larger than the package's mass.")
            fraction_to_subtract = other / self.get_mass()
            result = MaterialPackage(
                self.material, self.size_class_masses * fraction_to_subtract)
            self.size_class_masses = self.size_class_masses * (
                1.0 - fraction_to_subtract)
            return result

        # Extract the specified mass of the specified size class.
        elif self._is_size_class_mass_tuple(other):
            index = self.material.get_size_class_index(other[0])
            if other[1] > self.size_class_masses[index]:
                raise Exception(
                    "Invalid extraction operation. "
                    "Cannot extract a size class mass larger than what the "
                    "package contains.")
            self.size_class_masses[index] = \
                self.size_class_masses[index] - other[1]
            resultarray = self.size_class_masses*0.0
            resultarray[index] = other[1]
            result = MaterialPackage(self.material, resultarray)
            return result

        # Extract all of the specified size class.
        elif type(other) is str:
            index = self.material.get_size_class_index(float(other))
            result = self * 0.0
            result.size_class_masses[index] = self.size_class_masses[index]
            self.size_class_masses[index] = 0.0
            return result

        # If not one of the above, it must be an invalid argument.
        else:
            raise TypeError("Invalid extraction argument.")