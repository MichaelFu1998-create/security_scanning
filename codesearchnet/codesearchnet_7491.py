def p_sequenceSimpleSyntax(self, p):
        """sequenceSimpleSyntax : INTEGER anySubType
                                | INTEGER32 anySubType
                                | OCTET STRING anySubType
                                | OBJECT IDENTIFIER anySubType"""
        n = len(p)
        if n == 3:
            p[0] = p[1]  # XXX not supporting subtypes here
        elif n == 4:
            p[0] = p[1] + ' ' + p[2]