def playstyles(self, year=2019):
        """Return all playstyles in dict {id0: playstyle0, id1: playstyle1}.

        :params year: Year.
        """
        if not self._playstyles:
            self._playstyles = playstyles()
        return self._playstyles