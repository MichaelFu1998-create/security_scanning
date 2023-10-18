def match(self, subsetLines, offsetOfSubset, fileName):
        """
            Search through lines for match.
            Raise an Exception if fail to match
            If match is succesful return the position the match was found
        """

        for (offset,l) in enumerate(subsetLines):
            column = l.find(self.literal)
            if column != -1:
                truePosition = offset + offsetOfSubset
                _logger.debug('Found match on line {}, col {}'.format(str(truePosition+ 1), column))
                _logger.debug('Line is {}'.format(l))
                self.matchLocation = CheckFileParser.FileLocation(fileName, truePosition +1)
                return truePosition

        # No Match found
        self.failed = True
        raise DirectiveException(self)