def p_VarTypes(self, p):
        """VarTypes : VarTypes ',' VarType
                    | VarType"""
        n = len(p)
        if n == 4:
            p[0] = ('VarTypes', p[1][1] + [p[3]])
        elif n == 2:
            p[0] = ('VarTypes', [p[1]])