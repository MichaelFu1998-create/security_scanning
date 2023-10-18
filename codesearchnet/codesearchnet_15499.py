def replace_variables(self, tokens, scope):
        """ Replace variables in tokenlist
        args:
            tokens (list): tokenlist
            scope (Scope): Current scope
        returns:
            list
        """
        list = []
        for t in tokens:
            if utility.is_variable(t):
                list.append(scope.swap(t))
            elif str(type(t)) == "<class 'lesscpy.plib.variable.Variable'>":
                list.append(scope.swap(t.name))
            else:
                list.append(t)
        return list