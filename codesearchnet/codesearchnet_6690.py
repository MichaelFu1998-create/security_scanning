def UNIFAC_Dortmund_groups(self):
        r'''Dictionary of Dortmund UNIFAC subgroup: count groups for the
        Dortmund UNIFAC subgroups, as determined by `DDBST's online service <http://www.ddbst.com/unifacga.html>`_.

        Examples
        --------
        >>> pprint(Chemical('Cumene').UNIFAC_Dortmund_groups)
        {1: 2, 9: 5, 13: 1}
        '''
        if self.__UNIFAC_Dortmund_groups:
            return self.__UNIFAC_Dortmund_groups
        else:
            load_group_assignments_DDBST()
            if self.InChI_Key in DDBST_MODIFIED_UNIFAC_assignments:
                self.__UNIFAC_Dortmund_groups = DDBST_MODIFIED_UNIFAC_assignments[self.InChI_Key]
                return self.__UNIFAC_Dortmund_groups
            else:
                return None