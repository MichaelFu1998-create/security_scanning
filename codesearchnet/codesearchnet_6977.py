def mass_fractions(self):
        r'''Dictionary of mass fractions for each atom in the mixture.

        Examples
        --------
        >>> Mixture(['CO2', 'O2'], zs=[0.5, 0.5]).mass_fractions
        {'C': 0.15801826905745822, 'O': 0.8419817309425419}
        '''
        things = dict()
        for zi, atoms in zip(self.zs, self.atomss):
            for atom, count in atoms.iteritems():
                if atom in things:
                    things[atom] += zi*count
                else:
                    things[atom] = zi*count
        return mass_fractions(things)