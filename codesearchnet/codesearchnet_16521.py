def __field(self):
        """Level-2 parser for a DX field object.

        pattern:
        object "site map 1" class field
        component "positions" value 1
        component "connections" value 2
        component "data" value 3
        """
        try:
            tok = self.__consume()
        except DXParserNoTokens:
            return

        if tok.equals('component'):
            component = self.__consume().value()
            if not self.__consume().equals('value'):
                raise DXParseError('field: "value" expected')
            classid = self.__consume().value()
            try:
                self.currentobject['components'][component] = classid
            except KeyError:
                self.currentobject['components'] = {component:classid}
        else:
            raise DXParseError('field: '+str(tok)+' not recognized.')