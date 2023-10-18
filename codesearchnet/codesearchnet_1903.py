def print_stmt(self, print_loc, stmt):
        """
        (2.6-2.7)
        print_stmt: 'print' ( [ test (',' test)* [','] ] |
                              '>>' test [ (',' test)+ [','] ] )
        """
        stmt.keyword_loc = print_loc
        if stmt.loc is None:
            stmt.loc = print_loc
        else:
            stmt.loc = print_loc.join(stmt.loc)
        return stmt