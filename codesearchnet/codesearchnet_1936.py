def yield_expr__26(self, yield_loc, exprs):
        """(2.6, 2.7, 3.0, 3.1, 3.2) yield_expr: 'yield' [testlist]"""
        if exprs is not None:
            return ast.Yield(value=exprs,
                             yield_loc=yield_loc, loc=yield_loc.join(exprs.loc))
        else:
            return ast.Yield(value=None,
                             yield_loc=yield_loc, loc=yield_loc)