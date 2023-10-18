def parse(self, scope):
        """ Parse function
        args:
            scope (Scope): Scope object
        returns:
            self
        """
        self.name, _, self.value = self.tokens
        if isinstance(self.name, tuple):
            if len(self.name) > 1:
                self.name, pad = self.name
                self.value.append(pad)
            else:
                self.name = self.name[0]
        scope.add_variable(self)
        return self