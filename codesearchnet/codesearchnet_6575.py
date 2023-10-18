def leagues(self, year=2019):
        """Return all leagues in dict {id0: league0, id1: league1}.

        :params year: Year.
        """
        if year not in self._leagues:
            self._leagues[year] = leagues(year)
        return self._leagues[year]