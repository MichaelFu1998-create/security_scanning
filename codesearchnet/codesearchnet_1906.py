def yield_stmt(self, expr):
        """yield_stmt: yield_expr"""
        return ast.Expr(value=expr, loc=expr.loc)