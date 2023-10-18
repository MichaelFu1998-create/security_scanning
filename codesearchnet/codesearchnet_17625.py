def get_element_mfr_dictionary(self):
        """
        Determine the mass flow rates of elements in the stream and return as
        a dictionary.

        :returns: Dictionary of element symbols and mass flow rates. [kg/h]
        """

        element_symbols = self.material.elements
        element_mfrs = self.get_element_mfrs()
        result = dict()
        for s, mfr in zip(element_symbols, element_mfrs):
            result[s] = mfr
        return result