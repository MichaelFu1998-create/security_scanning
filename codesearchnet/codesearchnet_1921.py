def try_stmt(self, try_loc, try_colon_loc, body, stmt):
        """
        try_stmt: ('try' ':' suite
                   ((except_clause ':' suite)+
                    ['else' ':' suite]
                    ['finally' ':' suite] |
                    'finally' ':' suite))
        """
        stmt.keyword_loc, stmt.try_colon_loc, stmt.body = \
            try_loc, try_colon_loc, body
        stmt.loc = stmt.loc.join(try_loc)
        return stmt