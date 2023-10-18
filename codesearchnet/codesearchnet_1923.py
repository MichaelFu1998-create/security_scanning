def with_stmt__27(self, with_loc, items, colon_loc, body):
        """(2.7, 3.1-) with_stmt: 'with' with_item (',' with_item)*  ':' suite"""
        return ast.With(items=items, body=body,
                        keyword_loc=with_loc, colon_loc=colon_loc,
                        loc=with_loc.join(body[-1].loc))