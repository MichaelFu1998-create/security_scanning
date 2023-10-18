def extract(self, other):
        """
        Extract 'other' from this stream, modifying this stream and returning
        the extracted material as a new stream.

        :param other: Can be one of the following:

          * float: A mass flow rate equal to other is extracted from self. Self
            is reduced by other and the extracted stream is returned as
            a new stream.
          * tuple (compound, mass): The other tuple specifies the mass flow
            rate of a compound to be extracted. It is extracted from self and
            the extracted mass flow rate is returned as a new stream.
          * string: The 'other' string specifies the compound to be
            extracted. All of the mass flow rate of that compound will be
            removed from self and a new stream created with it.
          * Material: The 'other' material specifies the list of
            compounds to extract.


        :returns: New MaterialStream object.
        """

        # Extract the specified mass flow rate.
        if type(other) is float or \
           type(other) is numpy.float64 or \
           type(other) is numpy.float32:
            return self._extract_mfr(other)

        # Extract the specified mass flow rateof the specified compound.
        elif self._is_compound_mfr_tuple(other):
            return self._extract_compound_mfr(other[0], other[1])

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