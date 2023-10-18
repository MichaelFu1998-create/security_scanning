def p_CreationPart(self, p):
        """CreationPart : CREATION_REQUIRES '{' Cells '}'
                        | CREATION_REQUIRES '{' '}'
                        | empty"""
        n = len(p)
        if n == 5:
            p[0] = (p[1], p[3])