def star_expr__30(self, star_opt, expr):
        """(3.0, 3.1) star_expr: ['*'] expr"""
        if star_opt:
            return ast.Starred(value=expr, ctx=None,
                               star_loc=star_opt, loc=expr.loc.join(star_opt))
        return expr