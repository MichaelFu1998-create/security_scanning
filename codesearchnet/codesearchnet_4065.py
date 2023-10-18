def t_hexnumber(self, t):
        r'-?0[xX][0-9a-fA-F]+'
        t.value = int(t.value, base=16)
        t.type = 'NUMBER'
        return t