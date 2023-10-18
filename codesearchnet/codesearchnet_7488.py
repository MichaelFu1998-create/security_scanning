def p_ObjectSyntax(self, p):
        """ObjectSyntax : SimpleSyntax
                        | conceptualTable
                        | row
                        | entryType
                        | ApplicationSyntax
                        | typeTag SimpleSyntax"""
        n = len(p)
        if n == 2:
            p[0] = p[1]
        elif n == 3:
            p[0] = p[2]