def __object(self):
        """Level-1 parser for objects.

        pattern: 'object' id 'class' type ...

        id ::=   integer|string|'"'white space string'"'
        type ::= string
        """
        self.__consume()                    # 'object'
        classid = self.__consume().text
        word = self.__consume().text
        if word != "class":
            raise DXParseError("reserved word %s should have been 'class'." % word)
        # save previous DXInitObject
        if self.currentobject:
            self.objects.append(self.currentobject)
        # setup new DXInitObject
        classtype = self.__consume().text
        self.currentobject = DXInitObject(classtype=classtype,classid=classid)

        self.use_parser(classtype)