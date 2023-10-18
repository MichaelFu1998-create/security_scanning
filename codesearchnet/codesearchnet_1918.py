def if_stmt(self, if_loc, test, if_colon_loc, body, elifs, else_opt):
        """if_stmt: 'if' test ':' suite ('elif' test ':' suite)* ['else' ':' suite]"""
        stmt = ast.If(orelse=[],
                      else_loc=None, else_colon_loc=None)

        if else_opt:
            stmt.else_loc, stmt.else_colon_loc, stmt.orelse = else_opt

        for elif_ in reversed(elifs):
            stmt.keyword_loc, stmt.test, stmt.if_colon_loc, stmt.body = elif_
            stmt.loc = stmt.keyword_loc.join(stmt.body[-1].loc)
            if stmt.orelse:
                stmt.loc = stmt.loc.join(stmt.orelse[-1].loc)
            stmt = ast.If(orelse=[stmt],
                          else_loc=None, else_colon_loc=None)

        stmt.keyword_loc, stmt.test, stmt.if_colon_loc, stmt.body = \
            if_loc, test, if_colon_loc, body
        stmt.loc = stmt.keyword_loc.join(stmt.body[-1].loc)
        if stmt.orelse:
            stmt.loc = stmt.loc.join(stmt.orelse[-1].loc)
        return stmt