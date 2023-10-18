def atom_fractions(self):
        r'''Dictionary of atom:fractional occurence of the elements in a
        chemical. Useful when performing element balances. For mass-fraction
        occurences, see :obj:`mass_fractions`.

        Examples
        --------
        >>> Chemical('Ammonium aluminium sulfate').atom_fractions
        {'H': 0.25, 'S': 0.125, 'Al': 0.0625, 'O': 0.5, 'N': 0.0625}
        '''
        if self.__atom_fractions:
            return self.__atom_fractions
        else:
            self.__atom_fractions = atom_fractions(self.atoms)
            return self.__atom_fractions