def _print_general_vs_table(self, idset1, idset2):
        """
        :param idset1:
        :param idset2:
        """
        ref1name = ''
        set1_hasref = isinstance(idset1, idset_with_reference)
        if set1_hasref:
            ref1arr = np.array(idset1.reflst)
            ref1name = idset1.refname

        ref2name = ref1name
        set2_hasref = isinstance(idset2, idset_with_reference)
        if set2_hasref:
            ref2arr = np.array(idset2.reflst)
            ref2name = idset2.refname
        else:
            ref2name = ref1name

        #First show a general table
        hdr11 = '{0} > {1}'.format(idset1.name, idset2.name)
        hdr12 = '{0} > {1} {2}'.format(idset1.name, idset2.name, ref2name)
        hdr13 = '{0} < {1}'.format(idset1.name, idset2.name)
        hdr14 = '{0} < {1} {2}'.format(idset1.name, idset2.name, ref1name)
        table = [[hdr11, hdr12, hdr13, hdr14]]

        set1 = set(idset1)
        set2 = set(idset2)
        row11 = list(set1 - set2)
        if set1_hasref:
            row12 = [ref1arr[np.where(idset1 == nom)][0] for nom in row11]
        else:
            row12 = ['Not found' for _ in row11]

        row13 = list(set2 - set1)
        if set2_hasref:
            row14 = [ref2arr[np.where(idset2 == nom)][0] for nom in row13]
        else:
            row14 = ['Not found' for _ in row13]

        tablst = self._tabulate_4_lists(row11, row12, row13, row14)
        table.extend(tablst)

        if len(table) > 1:
            print(tabulate(table, headers='firstrow'))
            print('\n')