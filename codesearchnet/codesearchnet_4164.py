def t_KEYWORD_AS_TAG(self, t):
        r'[a-zA-Z]+'
        t.type = self.reserved.get(t.value, 'UNKNOWN_TAG')
        t.value = t.value.strip()
        return t