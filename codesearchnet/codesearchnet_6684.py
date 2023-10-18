def Hill(self):
        r'''Hill formula of a compound. For a description of the Hill system,
        see :obj:`thermo.elements.atoms_to_Hill`.

        Examples
        --------
        >>> Chemical('furfuryl alcohol').Hill
        'C5H6O2'
        '''
        if self.__Hill:
            return self.__Hill
        else:
            self.__Hill = atoms_to_Hill(self.atoms)
            return self.__Hill