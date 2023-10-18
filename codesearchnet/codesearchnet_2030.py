def findall(self, string, pos=0, endpos=sys.maxint):
        """Return a list of all non-overlapping matches of pattern in string."""
        matchlist = []
        state = _State(string, pos, endpos, self.flags)
        while state.start <= state.end:
            state.reset()
            state.string_position = state.start
            if not state.search(self._code):
                break
            match = SRE_Match(self, state)
            if self.groups == 0 or self.groups == 1:
                item = match.group(self.groups)
            else:
                item = match.groups("")
            matchlist.append(item)
            if state.string_position == state.start:
                state.start += 1
            else:
                state.start = state.string_position
        return matchlist