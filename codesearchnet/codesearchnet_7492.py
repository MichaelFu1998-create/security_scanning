def p_ApplicationSyntax(self, p):
        """ApplicationSyntax : IPADDRESS anySubType
                             | COUNTER32
                             | COUNTER32 integerSubType
                             | GAUGE32
                             | GAUGE32 integerSubType
                             | UNSIGNED32
                             | UNSIGNED32 integerSubType
                             | TIMETICKS anySubType
                             | OPAQUE
                             | OPAQUE octetStringSubType
                             | COUNTER64
                             | COUNTER64 integerSubType"""
        # COUNTER32 and COUNTER64 was with anySubType in libsmi
        n = len(p)
        if n == 2:
            p[0] = ('ApplicationSyntax', p[1])
        elif n == 3:
            p[0] = ('ApplicationSyntax', p[1], p[2])