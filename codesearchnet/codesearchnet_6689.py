def UNIFAC_groups(self):
        r'''Dictionary of UNIFAC subgroup: count groups for the original
        UNIFAC subgroups, as determined by `DDBST's online service <http://www.ddbst.com/unifacga.html>`_.

        Examples
        --------
        >>> pprint(Chemical('Cumene').UNIFAC_groups)
        {1: 2, 9: 5, 13: 1}
        '''
        if self.__UNIFAC_groups:
            return self.__UNIFAC_groups
        else:
            load_group_assignments_DDBST()
            if self.InChI_Key in DDBST_UNIFAC_assignments:
                self.__UNIFAC_groups = DDBST_UNIFAC_assignments[self.InChI_Key]
                return self.__UNIFAC_groups
            else:
                return None