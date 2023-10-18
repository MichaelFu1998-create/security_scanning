def parse(self, scope):
        """ Parse Node
        args:
            scope (Scope): Scope object
        raises:
            SyntaxError
        returns:
            str
        """
        assert (len(self.tokens) == 3)
        expr = self.process(self.tokens, scope)
        A, O, B = [
            e[0] if isinstance(e, tuple) else e for e in expr
            if str(e).strip()
        ]
        try:
            a, ua = utility.analyze_number(A, 'Illegal element in expression')
            b, ub = utility.analyze_number(B, 'Illegal element in expression')
        except SyntaxError:
            return ' '.join([str(A), str(O), str(B)])
        if (a is False or b is False):
            return ' '.join([str(A), str(O), str(B)])
        if ua == 'color' or ub == 'color':
            return color.Color().process((A, O, B))
        if a == 0 and O == '/':
            # NOTE(saschpe): The ugliest but valid CSS since sliced bread: 'font: 0/1 a;'
            return ''.join([str(A), str(O), str(B), ' '])
        out = self.operate(a, b, O)
        if isinstance(out, bool):
            return out
        return self.with_units(out, ua, ub)