def atom_fractions(self):
        r'''Dictionary of atomic fractions for each atom in the mixture.

        Examples
        --------
        >>> Mixture(['CO2', 'O2'], zs=[0.5, 0.5]).atom_fractions
        {'C': 0.2, 'O': 0.8}
        '''
        things = dict()
        for zi, atoms in zip(self.zs, self.atomss):
            for atom, count in atoms.iteritems():
                if atom in things:
                    things[atom] += zi*count
                else:
                    things[atom] = zi*count

        tot = sum(things.values())
        return {atom : value/tot for atom, value in things.iteritems()}