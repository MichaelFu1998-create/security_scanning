def _transliterate(self, text, outFormat):
        """ Transliterate a devanagari text into the target format.
        
        Transliterating a character to or from Devanagari is not a simple 
        lookup: it depends on the preceding and following characters.
        """
        def getResult(): 
            if curMatch.isspace():
                result.append(curMatch)
                return
            if prevMatch in self:
                prev = self[prevMatch]
            else:
                prev = None
            if nextMatch in self:
                next = self[nextMatch]
            else:
                next = None
            try:
                equiv = outFormat._equivalent(self[curMatch], 
                                                            prev, #self.get(prevMatch, None), 
                                                            next, #self.get(nextMatch, None),
                                                            self._implicitA)
            except KeyError:
                equiv = _unrecognised(curMatch)
            for e in equiv:
                result.append(e)
                
        def incr(c):
            if self._longestEntry == 1:
                return 1
            return len(c)
            
            
        result = []
        text = self._preprocess(text)
        i = 0
        prevMatch = None
        nextMatch = None
        curMatch = self._getNextChar(text, i)
        i = i + len(curMatch)
        while i < len(text):
            nextMatch = self._getNextChar(text, i)
            getResult()
            i = i + len(nextMatch)
            prevMatch = curMatch
            curMatch = nextMatch
            nextMatch = None
        getResult() 
        return result