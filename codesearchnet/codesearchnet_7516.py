def p_Cells(self, p):
        """Cells : Cells ',' Cell
                 | Cell"""
        n = len(p)
        if n == 4:
            p[0] = ('Cells', p[1][1] + [p[3]])
        elif n == 2:
            p[0] = ('Cells', [p[1]])