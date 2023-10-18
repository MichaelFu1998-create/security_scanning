def charge(self):
        '''Charge of the species as an integer. Computed as a property as most
        species do not have a charge and so storing it would be a waste of 
        memory.
        '''
        try:
            return self._charge
        except AttributeError:
            self._charge = charge_from_formula(self.formula)
            return self._charge