def p_sequenceApplicationSyntax(self, p):
        """sequenceApplicationSyntax : IPADDRESS anySubType
                                     | COUNTER32 anySubType
                                     | GAUGE32 anySubType
                                     | UNSIGNED32 anySubType
                                     | TIMETICKS anySubType
                                     | OPAQUE
                                     | COUNTER64 anySubType"""
        n = len(p)
        if n == 2:
            p[0] = p[1]
        elif n == 3:
            p[0] = p[1]