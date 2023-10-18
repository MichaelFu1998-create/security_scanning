def p_importIdentifiers(self, p):
        """importIdentifiers : importIdentifiers ',' importIdentifier
                             | importIdentifier"""
        n = len(p)
        if n == 4:
            p[0] = p[1] + [p[3]]
        elif n == 2:
            p[0] = [p[1]]