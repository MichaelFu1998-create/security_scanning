def t_NUMBER(self, t):
        r'-?[0-9]+'
        t.value = int(t.value)
        neg = 0
        if t.value < 0:
            neg = 1

        val = abs(t.value)

        if val <= UNSIGNED32_MAX:
            if neg:
                t.type = 'NEGATIVENUMBER'

        elif val <= UNSIGNED64_MAX:
            if neg:
                t.type = 'NEGATIVENUMBER64'
            else:
                t.type = 'NUMBER64'

        else:
            raise error.PySmiLexerError("Number %s is too big" % t.value, lineno=t.lineno)

        return t