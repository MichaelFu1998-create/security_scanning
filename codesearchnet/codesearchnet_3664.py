def declarations(self):
        """ Returns the variable expressions of this constraint set """
        declarations = GetDeclarations()
        for a in self.constraints:
            try:
                declarations.visit(a)
            except RuntimeError:
                # TODO: (defunct) move recursion management out of PickleSerializer
                if sys.getrecursionlimit() >= PickleSerializer.MAX_RECURSION:
                    raise Exception(f'declarations recursion limit surpassed {PickleSerializer.MAX_RECURSION}, aborting')
                new_limit = sys.getrecursionlimit() + PickleSerializer.DEFAULT_RECURSION
                if new_limit <= PickleSerializer.DEFAULT_RECURSION:
                    sys.setrecursionlimit(new_limit)
                    return self.declarations
        return declarations.result