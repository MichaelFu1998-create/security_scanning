def teams(self, year=2019):
        """Return all teams in dict {id0: team0, id1: team1}.

        :params year: Year.
        """
        if year not in self._teams:
            self._teams[year] = teams(year)
        return self._teams[year]