def charge(self):
        r'''Charge of a chemical, computed with RDKit from a chemical's SMILES.
        If RDKit is not available, holds None.

        Examples
        --------
        >>> Chemical('sodium ion').charge
        1
        '''
        try:
            if not self.rdkitmol:
                return charge_from_formula(self.formula)
            else:
                return Chem.GetFormalCharge(self.rdkitmol)
        except:
            return charge_from_formula(self.formula)