def return_stmt(self, stmt_loc, values):
        """return_stmt: 'return' [testlist]"""
        loc = stmt_loc
        if values:
            loc = loc.join(values.loc)
        return ast.Return(value=values,
                          loc=loc, keyword_loc=stmt_loc)