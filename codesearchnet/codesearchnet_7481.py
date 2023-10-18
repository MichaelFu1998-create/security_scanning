def p_sequenceItems(self, p):
        """sequenceItems : sequenceItems ',' sequenceItem
                         | sequenceItem"""
        # libsmi: TODO: might this list be emtpy?
        n = len(p)
        if n == 4:
            p[0] = p[1] + [p[3]]
        elif n == 2:
            p[0] = [p[1]]