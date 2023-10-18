def for_stmt(self, for_loc, target, in_loc, iter, for_colon_loc, body, else_opt):
        """for_stmt: 'for' exprlist 'in' testlist ':' suite ['else' ':' suite]"""
        stmt = ast.For(target=self._assignable(target), iter=iter, body=body, orelse=[],
                       keyword_loc=for_loc, in_loc=in_loc, for_colon_loc=for_colon_loc,
                       else_loc=None, else_colon_loc=None,
                       loc=for_loc.join(body[-1].loc))
        if else_opt:
            stmt.else_loc, stmt.else_colon_loc, stmt.orelse = else_opt
            stmt.loc = stmt.loc.join(stmt.orelse[-1].loc)

        return stmt