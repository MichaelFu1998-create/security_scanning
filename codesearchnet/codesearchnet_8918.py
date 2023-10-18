def union(self, a, b):
        """Merges the set that contains ``a`` with the set that contains ``b``.

        Parameters
        ----------
        a, b : objects
            Two objects whose sets are to be merged.
        """
        s1, s2 = self.find(a), self.find(b)
        if s1 != s2:
            r1, r2  = self._rank[s1], self._rank[s2]
            if r2 > r1:
                r1, r2 = r2, r1
                s1, s2 = s2, s1
            if r1 == r2:
                self._rank[s1] += 1

            self._leader[s2] = s1
            self._size[s1]  += self._size[s2]
            self.nClusters  -= 1