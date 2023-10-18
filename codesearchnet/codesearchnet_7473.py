def t_HEX_STRING(self, t):
        r'\'[0-9a-fA-F]*\'[hH]'
        value = t.value[1:-2]
        while value and value[0] == '0' and len(value) % 2:
            value = value[1:]
        # XXX raise in strict mode
        #    if len(value) % 2:
        #      raise error.PySmiLexerError("Number of symbols have to be even in hex string %s" % t.value, lineno=t.lineno)
        return t