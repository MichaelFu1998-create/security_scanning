def _print_foreign_repetition_table(self, idset1, idset2):
        """
        :param idset1:
        :param idset2:
        """

        assert(isinstance(idset1, idset_with_reference))
        assert(isinstance(idset2, idset))

        reps = idset2.get_repetitions()
        if len(reps) < 1:
            return

        refs = np.array(idset1.reflst)
        table = [['{0} {1} values of repetitions in {2}'.format(idset1.name,
                                                                idset1.refname,
                                                                idset2.name),
                  '']]

        for rep in reps:
            if np.any(idset1 == rep):
                matches = refs[np.where(idset1 == rep)]
                myrep = rep
                for m in matches:
                    table.append([myrep, m])
                    myrep = ''

        print(tabulate(table, headers='firstrow'))
        print('\n')