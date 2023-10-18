def _sorted_copy(self, comparison, reversed=False):
        """
        Returns a sorted copy with the colors arranged according to the given comparison.
        """
        sorted = self.copy()
        _list.sort(sorted, comparison)
        if reversed:
            _list.reverse(sorted)
        return sorted