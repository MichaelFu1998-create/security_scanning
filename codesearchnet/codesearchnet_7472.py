def t_BIN_STRING(self, t):
        r'\'[01]*\'[bB]'
        value = t.value[1:-2]
        while value and value[0] == '0' and len(value) % 8:
            value = value[1:]
        # XXX raise in strict mode
        #    if len(value) % 8:
        #      raise error.PySmiLexerError("Number of 0s and 1s have to divide by 8 in binary string %s" % t.value, lineno=t.lineno)
        return t