def p_Compliances(self, p):
        """Compliances : Compliances Compliance
                       | Compliance"""
        n = len(p)
        if n == 3:
            p[0] = p[1] and p[2] and ('Compliances', p[1][1] + [p[2]]) or p[1]
        elif n == 2:
            p[0] = p[1] and ('Compliances', [p[1]]) or None