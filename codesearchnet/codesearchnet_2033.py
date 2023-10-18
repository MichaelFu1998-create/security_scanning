def split(self, string, maxsplit=0):
        """Split string by the occurrences of pattern."""
        splitlist = []
        state = _State(string, 0, sys.maxint, self.flags)
        n = 0
        last = state.start
        while not maxsplit or n < maxsplit:
            state.reset()
            state.string_position = state.start
            if not state.search(self._code):
                break
            if state.start == state.string_position: # zero-width match
                if last == state.end:                # or end of string
                    break
                state.start += 1
                continue
            splitlist.append(string[last:state.start])
            # add groups (if any)
            if self.groups:
                match = SRE_Match(self, state)
                # TODO: Use .extend once it is implemented.
                # splitlist.extend(list(match.groups(None)))
                splitlist += (list(match.groups(None)))
            n += 1
            last = state.start = state.string_position
        splitlist.append(string[last:state.end])
        return splitlist