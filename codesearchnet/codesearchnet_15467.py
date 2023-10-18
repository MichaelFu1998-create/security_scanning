def copy_inner(self, scope):
        """Copy block contents (properties, inner blocks).
        Renames inner block from current scope.
        Used for mixins.
        args:
            scope (Scope): Current scope
        returns:
            list (block contents)
        """
        if self.tokens[1]:
            tokens = [u.copy() if u else u for u in self.tokens[1]]
            out = [p for p in tokens if p]
            utility.rename(out, scope, Block)
            return out
        return None