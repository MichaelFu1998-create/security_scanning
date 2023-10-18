def print_compare_idsets_one_ref(self, idset1_name, idset2_name):
        """
        idset1_name: string
        key of an idset_with_reference

        idset2_name: string
        key of an idset
        """
        try:
            idset1 = self[idset1_name]
            idset2 = self[idset2_name]
        except KeyError as ke:
            log.error('Error compare_idsets: getting keys {0} and {1}'.format(idset1_name,
                                                                              idset2_name))
            import sys, pdb
            pdb.post_mortem(sys.exc_info()[2])
            raise

        assert(isinstance(idset1, idset_with_reference))
        assert(isinstance(idset2, idset))

        self._print_general_vs_table(idset1, idset2)
        self._print_foreign_repetition_table(idset1, idset2)