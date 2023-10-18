def concretize(self, symbolic, policy, maxcount=7):
        """ This finds a set of solutions for symbolic using policy.
            This raises TooManySolutions if more solutions than maxcount
        """
        assert self.constraints == self.platform.constraints
        symbolic = self.migrate_expression(symbolic)

        vals = []
        if policy == 'MINMAX':
            vals = self._solver.minmax(self._constraints, symbolic)
        elif policy == 'MAX':
            vals = self._solver.max(self._constraints, symbolic)
        elif policy == 'MIN':
            vals = self._solver.min(self._constraints, symbolic)
        elif policy == 'SAMPLED':
            m, M = self._solver.minmax(self._constraints, symbolic)
            vals += [m, M]
            if M - m > 3:
                if self._solver.can_be_true(self._constraints, symbolic == (m + M) // 2):
                    vals.append((m + M) // 2)
            if M - m > 100:
                for i in (0, 1, 2, 5, 32, 64, 128, 320):
                    if self._solver.can_be_true(self._constraints, symbolic == m + i):
                        vals.append(m + i)
                    if maxcount <= len(vals):
                        break
            if M - m > 1000 and maxcount > len(vals):
                vals += self._solver.get_all_values(self._constraints, symbolic,
                                                    maxcnt=maxcount - len(vals), silent=True)
        elif policy == 'ONE':
            vals = [self._solver.get_value(self._constraints, symbolic)]
        else:
            assert policy == 'ALL'
            vals = solver.get_all_values(self._constraints, symbolic, maxcnt=maxcount, silent=True)

        return tuple(set(vals))