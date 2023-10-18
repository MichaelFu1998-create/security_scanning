def expr_stmt(self, lhs, rhs):
        """
        (2.6, 2.7, 3.0, 3.1)
        expr_stmt: testlist (augassign (yield_expr|testlist) |
                             ('=' (yield_expr|testlist))*)
        (3.2-)
        expr_stmt: testlist_star_expr (augassign (yield_expr|testlist) |
                             ('=' (yield_expr|testlist_star_expr))*)
        """
        if isinstance(rhs, ast.AugAssign):
            if isinstance(lhs, ast.Tuple) or isinstance(lhs, ast.List):
                error = diagnostic.Diagnostic(
                    "fatal", "illegal expression for augmented assignment", {},
                    rhs.op.loc, [lhs.loc])
                self.diagnostic_engine.process(error)
            else:
                rhs.target = self._assignable(lhs)
                rhs.loc = rhs.target.loc.join(rhs.value.loc)
                return rhs
        elif rhs is not None:
            rhs.targets = list(map(self._assignable, [lhs] + rhs.targets))
            rhs.loc = lhs.loc.join(rhs.value.loc)
            return rhs
        else:
            return ast.Expr(value=lhs, loc=lhs.loc)