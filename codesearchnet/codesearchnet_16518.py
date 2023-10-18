def __gridpositions(self):
        """Level-2 parser for gridpositions.

        pattern:
        object 1 class gridpositions counts 97 93 99
        origin -46.5 -45.5 -48.5
        delta 1 0 0
        delta 0 1 0
        delta 0 0 1
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
                raise DXParseError('gridpositions: no shape parameters')
            self.currentobject['shape'] = shape
        elif tok.equals('origin'):
            origin = []
            try:
                while (self.__peek().iscode('INTEGER') or
                       self.__peek().iscode('REAL')):
                    tok = self.__consume()
                    origin.append(tok.value())
            except DXParserNoTokens:
                pass
            if len(origin) == 0:
                raise DXParseError('gridpositions: no origin parameters')
            self.currentobject['origin'] = origin
        elif tok.equals('delta'):
            d = []
            try:
                while (self.__peek().iscode('INTEGER') or
                       self.__peek().iscode('REAL')):
                    tok = self.__consume()
                    d.append(tok.value())
            except DXParserNoTokens:
                pass
            if len(d) == 0:
                raise DXParseError('gridpositions: missing delta parameters')
            try:
                self.currentobject['delta'].append(d)
            except KeyError:
                self.currentobject['delta'] = [d]
        else:
            raise DXParseError('gridpositions: '+str(tok)+' not recognized.')