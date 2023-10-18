def _rc_msetnx(self, mapping):
        """
        Sets each key in the ``mapping`` dict to its corresponding value if
        none of the keys are already set
        """
        for k in iterkeys(mapping):
            if self.exists(k):
                return False

        return self._rc_mset(mapping)