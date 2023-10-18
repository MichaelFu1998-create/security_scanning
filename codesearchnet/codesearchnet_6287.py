def get_metabolite_compartments(self):
        """Return all metabolites' compartments."""
        warn('use Model.compartments instead', DeprecationWarning)
        return {met.compartment for met in self.metabolites
                if met.compartment is not None}