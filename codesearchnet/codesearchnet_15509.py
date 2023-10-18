def parse(self, scope):
        """Parse Node within scope.
        the functions ~( and e( map to self.escape
        and %( maps to self.sformat
        args:
            scope (Scope): Current scope
        """
        name = ''.join(self.tokens[0])
        parsed = self.process(self.tokens[1:], scope)

        if name == '%(':
            name = 'sformat'
        elif name in ('~', 'e'):
            name = 'escape'
        color = Color.Color()
        args = [
            t for t in parsed
            if not isinstance(t, string_types) or t not in '(),'
        ]
        if hasattr(self, name):
            try:
                return getattr(self, name)(*args)
            except ValueError:
                pass

        if hasattr(color, name):
            try:
                result = getattr(color, name)(*args)
                try:
                    return result + ' '
                except TypeError:
                    return result
            except ValueError:
                pass
        return name + ''.join([p for p in parsed])