def search(self, string, pos=0, endpos=sys.maxint):
        """Scan through string looking for a location where this regular
        expression produces a match, and return a corresponding MatchObject
        instance. Return None if no position in the string matches the
        pattern."""
        state = _State(string, pos, endpos, self.flags)
        if state.search(self._code):
            return SRE_Match(self, state)
        else:
            return None