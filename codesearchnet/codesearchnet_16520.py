def __array(self):
        """Level-2 parser for arrays.

        pattern:
        object 3 class array type double rank 0 items 12 data follows
        0 2 0
        0 0 3.6
        0 -2.0 1e-12
        +4.534e+01 .34534 0.43654
        attribute "dep" string "positions"
        """
        try:
            tok = self.__consume()
        except DXParserNoTokens:
            return

        if tok.equals('type'):
            tok = self.__consume()
            if not tok.iscode('STRING'):
                raise DXParseError('array: type was "%s", not a string.'%\
                                   tok.text)
            self.currentobject['type'] = tok.value()
        elif tok.equals('rank'):
            tok = self.__consume()
            try:
                self.currentobject['rank'] = tok.value('INTEGER')
            except ValueError:
                raise DXParseError('array: rank was "%s", not an integer.'%\
                                   tok.text)
        elif tok.equals('items'):
            tok = self.__consume()
            try:
                self.currentobject['size'] = tok.value('INTEGER')
            except ValueError:
                raise DXParseError('array: items was "%s", not an integer.'%\
                                   tok.text)
        elif tok.equals('data'):
            tok = self.__consume()
            if not tok.iscode('STRING'):
                raise DXParseError('array: data was "%s", not a string.'%\
                                   tok.text)
            if tok.text != 'follows':
                raise NotImplementedError(\
                            'array: Only the "data follows header" format is supported.')
            if not self.currentobject['size']:
                raise DXParseError("array: missing number of items")
            # This is the slow part.  Once we get here, we are just
            # reading in a long list of numbers.  Conversion to floats
            # will be done later when the numpy array is created.

            # Don't assume anything about whitespace or the number of elements per row
            self.currentobject['array'] = []
            while len(self.currentobject['array']) <self.currentobject['size']:
                 self.currentobject['array'].extend(self.dxfile.readline().strip().split())

            # If you assume that there are three elements per row
            # (except the last) the following version works and is a little faster.
            # for i in range(int(numpy.ceil(self.currentobject['size']/3))):
            #     self.currentobject['array'].append(self.dxfile.readline())
            # self.currentobject['array'] = ' '.join(self.currentobject['array']).split()
        elif tok.equals('attribute'):
            # not used at the moment
            attribute = self.__consume().value()
            if not self.__consume().equals('string'):
                raise DXParseError('array: "string" expected.')
            value = self.__consume().value()
        else:
            raise DXParseError('array: '+str(tok)+' not recognized.')