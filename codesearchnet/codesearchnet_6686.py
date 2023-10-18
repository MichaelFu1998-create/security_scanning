def mass_fractions(self):
        r'''Dictionary of atom:mass-weighted fractional occurence of elements.
        Useful when performing mass balances. For atom-fraction occurences, see
        :obj:`atom_fractions`.

        Examples
        --------
        >>> Chemical('water').mass_fractions
        {'H': 0.11189834407236524, 'O': 0.8881016559276347}
        '''
        if self.__mass_fractions:
            return self.__mass_fractions
        else:
            self.__mass_fractions =  mass_fractions(self.atoms, self.MW)
            return self.__mass_fractions