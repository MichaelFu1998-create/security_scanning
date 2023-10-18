def extract(self, other):
        """
        Extract 'other' from this package, modifying this package and
        returning the extracted material as a new package.

        :param other: Can be one of the following:

          * float: A mass equal to other is extracted from self. Self is
            reduced by other and the extracted package is returned as
            a new package.
          * tuple (compound, mass): The other tuple specifies the mass
            of a compound to be extracted. It is extracted from self and
            the extracted mass is returned as a new package.
          * string: The 'other' string specifies the compound to be
            extracted. All of the mass of that compound will be removed
            from self and a new package created with it.
          * Material: The 'other' material specifies the list of
            compounds to extract.


        :returns: New MaterialPackage object.
        """

        # Extract the specified mass.
        if type(other) is float or \
           type(other) is numpy.float64 or \
           type(other) is numpy.float32:
            return self._extract_mass(other)

        # Extract the specified mass of the specified compound.
        elif self._is_compound_mass_tuple(other):
            return self._extract_compound_mass(other[0], other[1])

        # Extract all of the specified compound.
        elif type(other) is str:
            return self._extract_compound(other)

        # TODO: Test
        # Extract all of the compounds of the specified material.
        elif type(other) is Material:
            return self._extract_material(other)

        # If not one of the above, it must be an invalid argument.
        else:
            raise TypeError("Invalid extraction argument.")