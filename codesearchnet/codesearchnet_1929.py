def star_expr__32(self, star_loc, expr):
        """(3.0-) star_expr: '*' expr"""
        return ast.Starred(value=expr, ctx=None,
                           star_loc=star_loc, loc=expr.loc.join(star_loc))