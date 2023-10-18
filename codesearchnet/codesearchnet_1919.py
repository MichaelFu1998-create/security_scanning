def while_stmt(self, while_loc, test, while_colon_loc, body, else_opt):
        """while_stmt: 'while' test ':' suite ['else' ':' suite]"""
        stmt = ast.While(test=test, body=body, orelse=[],
                         keyword_loc=while_loc, while_colon_loc=while_colon_loc,
                         else_loc=None, else_colon_loc=None,
                         loc=while_loc.join(body[-1].loc))
        if else_opt:
            stmt.else_loc, stmt.else_colon_loc, stmt.orelse = else_opt
            stmt.loc = stmt.loc.join(stmt.orelse[-1].loc)

        return stmt