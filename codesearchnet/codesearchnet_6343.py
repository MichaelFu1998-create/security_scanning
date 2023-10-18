def compartments(self):
        """lists compartments the metabolites are in"""
        if self._compartments is None:
            self._compartments = {met.compartment for met in self._metabolites
                                  if met.compartment is not None}
        return self._compartments