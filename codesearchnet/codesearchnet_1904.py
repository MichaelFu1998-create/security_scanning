def del_stmt(self, stmt_loc, exprs):
        # Python uses exprlist here, but does *not* obey the usual
        # tuple-wrapping semantics, so we embed the rule directly.
        """del_stmt: 'del' exprlist"""
        return ast.Delete(targets=[self._assignable(expr, is_delete=True) for expr in exprs],
                          loc=stmt_loc.join(exprs[-1].loc), keyword_loc=stmt_loc)