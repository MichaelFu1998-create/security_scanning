def p_Revisions(self, p):
        """Revisions : Revisions Revision
                     | Revision"""
        n = len(p)
        if n == 3:
            p[0] = ('Revisions', p[1][1] + [p[2]])
        elif n == 2:
            p[0] = ('Revisions', [p[1]])