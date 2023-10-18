def process(self, tokens, scope):
        """ Process tokenslist, flattening and parsing it
        args:
            tokens (list): tokenlist
            scope (Scope): Current scope
        returns:
            list
        """
        while True:
            tokens = list(utility.flatten(tokens))
            done = True
            if any(t for t in tokens if hasattr(t, 'parse')):
                tokens = [
                    t.parse(scope) if hasattr(t, 'parse') else t
                    for t in tokens
                ]
                done = False
            if any(
                    t for t in tokens
                    if (utility.is_variable(t)) or str(type(t)) ==
                    "<class 'lesscpy.plib.variable.Variable'>"):
                tokens = self.replace_variables(tokens, scope)
                done = False
            if done:
                break
        return tokens