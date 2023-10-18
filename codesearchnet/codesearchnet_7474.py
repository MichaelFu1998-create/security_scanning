def t_QUOTED_STRING(self, t):
        r'\"[^\"]*\"'
        t.lexer.lineno += len(re.findall(r'\r\n|\n|\r', t.value))
        return t