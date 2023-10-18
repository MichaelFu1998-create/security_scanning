def t_LINE_OR_KEYWORD_VALUE(self, t):
        r':.+'
        t.value = t.value[1:].strip()
        if t.value in self.reserved.keys():
            t.type = self.reserved[t.value]
        else:
            t.type = 'LINE'
        return t