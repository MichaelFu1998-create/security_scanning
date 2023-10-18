def parse(self, scope):
        """Parse node. Block identifiers are stored as
        strings with spaces replaced with ?
        args:
            scope (Scope): Current scope
        raises:
            SyntaxError
        returns:
            self
        """
        names = []
        name = []
        self._subp = ('@media', '@keyframes', '@-moz-keyframes',
                      '@-webkit-keyframes', '@-ms-keyframes')
        if self.tokens and hasattr(self.tokens, 'parse'):
            self.tokens = list(
                utility.flatten([
                    id.split() + [',']
                    for id in self.tokens.parse(scope).split(',')
                ]))
            self.tokens.pop()
        if self.tokens and any(hasattr(t, 'parse') for t in self.tokens):
            tmp_tokens = []
            for t in self.tokens:
                if hasattr(t, 'parse'):
                    tmp_tokens.append(t.parse(scope))
                else:
                    tmp_tokens.append(t)
            self.tokens = list(utility.flatten(tmp_tokens))
        if self.tokens and self.tokens[0] in self._subp:
            name = list(utility.flatten(self.tokens))
            self.subparse = True
        else:
            self.subparse = False
            for n in utility.flatten(self.tokens):
                if n == '*':
                    name.append('* ')
                elif n in '>+~':
                    if name and name[-1] == ' ':
                        name.pop()
                    name.append('?%s?' % n)
                elif n == ',':
                    names.append(name)
                    name = []
                else:
                    name.append(n)
        names.append(name)
        parsed = self.root(scope, names) if scope else names

        # Interpolated selectors need another step, we have to replace variables. Avoid reserved words though
        #
        # Example:  '.@{var}'       results in [['.', '@{var}']]
        # But:      '@media print'  results in [['@media', ' ', 'print']]
        #
        def replace_variables(tokens, scope):
            return [
                scope.swap(t)
                if (utility.is_variable(t) and not t in reserved.tokens) else t
                for t in tokens
            ]

        parsed = [
            list(utility.flatten(replace_variables(part, scope)))
            for part in parsed
        ]

        self.parsed = [[
            i for i, j in utility.pairwise(part)
            if i != ' ' or (j and '?' not in j)
        ] for part in parsed]
        return self