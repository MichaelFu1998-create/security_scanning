def __gridconnections(self):
        """Level-2 parser for gridconnections.

        pattern:
        object 2 class gridconnections counts 97 93 99
        """
        try:
            tok = self.__consume()
        except DXParserNoTokens:
            return

        if tok.equals('counts'):
            shape = []
            try:
                while True:
                    # raises exception if not an int
                    self.__peek().value('INTEGER')
                    tok = self.__consume()
                    shape.append(tok.value('INTEGER'))
            except (DXParserNoTokens, ValueError):
                pass
            if len(shape) == 0:
                raise DXParseError('gridconnections: no shape parameters')
            self.currentobject['shape'] = shape
        else:
            raise DXParseError('gridconnections: '+str(tok)+' not recognized.')