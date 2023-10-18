def _decompose_pattern(self, pattern):
        """
        Given a path pattern with format declaration, generates a
        four-tuple (glob_pattern, regexp pattern, fields, type map)
        """
        sep = '~lancet~sep~'
        float_codes = ['e','E','f', 'F','g', 'G', 'n']
        typecodes = dict([(k,float) for k in float_codes]
                         + [('b',bin), ('d',int), ('o',oct), ('x',hex)])
        parse = list(string.Formatter().parse(pattern))
        text, fields, codes, _ = zip(*parse)

        # Finding the field types from format string
        types = []
        for (field, code) in zip(fields, codes):
            if code in ['', None]: continue
            constructor =  typecodes.get(code[-1], None)
            if constructor: types += [(field, constructor)]

        stars =  ['' if not f else '*' for f in fields]
        globpat = ''.join(text+star for (text,star) in zip(text,stars))

        refields = ['' if not f else sep+('(?P<%s>.*?)'% f)+sep for f in fields]
        parts = ''.join(text+group for (text,group) in zip(text, refields)).split(sep)
        for i in range(0, len(parts), 2): parts[i] = re.escape(parts[i])

        regexp_pattern = ''.join(parts).replace('\\*','.*')
        fields = list(f for f in fields if f)
        return globpat, regexp_pattern , fields, dict(types)