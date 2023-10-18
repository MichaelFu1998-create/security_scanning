def p_SimpleSyntax(self, p):
        """SimpleSyntax : INTEGER
                        | INTEGER integerSubType
                        | INTEGER enumSpec
                        | INTEGER32
                        | INTEGER32 integerSubType
                        | UPPERCASE_IDENTIFIER enumSpec
                        | UPPERCASE_IDENTIFIER integerSubType
                        | OCTET STRING
                        | OCTET STRING octetStringSubType
                        | UPPERCASE_IDENTIFIER octetStringSubType
                        | OBJECT IDENTIFIER anySubType"""
        n = len(p)
        if n == 2:
            p[0] = ('SimpleSyntax', p[1])

        elif n == 3:
            if p[1] == 'OCTET':
                p[0] = ('SimpleSyntax', p[1] + ' ' + p[2])
            else:
                p[0] = ('SimpleSyntax', p[1], p[2])

        elif n == 4:
            p[0] = ('SimpleSyntax', p[1] + ' ' + p[2], p[3])