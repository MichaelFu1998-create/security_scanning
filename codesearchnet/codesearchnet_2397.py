def GetCachedPattern(self, patternId: int, cache: bool):
        """
        Get a pattern by patternId.
        patternId: int, a value in class `PatternId`.
        Return a pattern if it supports the pattern else None.
        cache: bool, if True, store the pattern for later use, if False, get a new pattern by `self.GetPattern`.
        """
        if cache:
            pattern = self._supportedPatterns.get(patternId, None)
            if pattern:
                return pattern
            else:
                pattern = self.GetPattern(patternId)
                if pattern:
                    self._supportedPatterns[patternId] = pattern
                    return pattern
        else:
            pattern = self.GetPattern(patternId)
            if pattern:
                self._supportedPatterns[patternId] = pattern
                return pattern