def match(self, subsetLines, offsetOfSubset, fileName):
        """
            Search through lines for match.
            Raise an Exception if a match
        """
        for (offset,l) in enumerate(subsetLines):
            for t in self.regex:
                m = t.Regex.search(l)
                if m != None:
                    truePosition = offset + offsetOfSubset
                    _logger.debug('Found match on line {}'.format(str(truePosition+ 1)))
                    _logger.debug('Line is {}'.format(l))
                    self.failed = True
                    self.matchLocation = CheckFileParser.FileLocation(fileName, truePosition +1)
                    raise DirectiveException(self)