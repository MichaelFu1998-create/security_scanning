def PSRK_groups(self):
        r'''Dictionary of PSRK subgroup: count groups for the PSRK subgroups,
        as determined by `DDBST's online service <http://www.ddbst.com/unifacga.html>`_.

        Examples
        --------
        >>> pprint(Chemical('Cumene').PSRK_groups)
        {1: 2, 9: 5, 13: 1}
        '''
        if self.__PSRK_groups:
            return self.__PSRK_groups
        else:
            load_group_assignments_DDBST()
            if self.InChI_Key in DDBST_PSRK_assignments:
                self.__PSRK_groups = DDBST_PSRK_assignments[self.InChI_Key]
                return self.__PSRK_groups
            else:
                return None