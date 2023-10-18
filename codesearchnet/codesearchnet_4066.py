def t_intnumber(self, t):
        r'-?\d+'
        t.value = int(t.value)
        t.type = 'NUMBER'
        return t