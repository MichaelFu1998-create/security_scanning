def extract(self, other):
        """
        Extract 'other' from self, modifying self and returning the extracted
        material as a new package.

        :param other: Can be one of the following:

          * float: A mass equal to other is extracted from self. Self is
            reduced by other and the extracted package is returned as a
            new package.
          * tuple (compound, mass): The other tuple specifies the mass of
            a compound to be extracted. It is extracted from self and the
            extracted mass is returned as a new package.
          * string: The 'other' string specifies the compound to be extracted.
            All of the mass of that compound will be removed from self and a
            new package created with it.


        :returns: A new material package containing the material that was
          extracted from self.
        """

        # Extract the specified mass.
        if type(other) is float:

            if other > self.get_mass():
                raise Exception('Invalid extraction operation. Cannot extract'
                                'a mass larger than the package\'s mass.')

            fraction_to_subtract = other / self.get_mass()
            result = MaterialPackage(
                self.material,
                [m * fraction_to_subtract for m in self.compound_masses])
            self.compound_masses = [m * (1.0 - fraction_to_subtract)
                                    for m in self.compound_masses]

            return result

        # Extract the specified mass of the specified compound.
        elif self._is_compound_mass_tuple(other):
            index = self.material.get_compound_index(other[0])

            if other[1] > self.compound_masses[index]:
                raise Exception('Invalid extraction operation. Cannot extract'
                                'a compound mass larger than what the package'
                                'contains.')

            self.compound_masses[index] -= other[1]
            resultarray = [0.0] * len(self.compound_masses)
            resultarray[index] = other[1]
            result = MaterialPackage(self.material, resultarray)

            return result

        # Extract all of the specified compound.
        elif type(other) is str:
            index = self.material.get_compound_index(other)
            result = self * 0.0
            result.compound_masses[index] = self.compound_masses[index]
            self.compound_masses[index] = 0.0

            return result

        # If not one of the above, it must be an invalid argument.
        else:
            raise TypeError('Invalid extraction argument.')