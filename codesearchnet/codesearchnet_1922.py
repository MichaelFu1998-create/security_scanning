def with_stmt__26(self, with_loc, context, with_var, colon_loc, body):
        """(2.6, 3.0) with_stmt: 'with' test [ with_var ] ':' suite"""
        if with_var:
            as_loc, optional_vars = with_var
            item = ast.withitem(context_expr=context, optional_vars=optional_vars,
                                as_loc=as_loc, loc=context.loc.join(optional_vars.loc))
        else:
            item = ast.withitem(context_expr=context, optional_vars=None,
                                as_loc=None, loc=context.loc)
        return ast.With(items=[item], body=body,
                        keyword_loc=with_loc, colon_loc=colon_loc,
                        loc=with_loc.join(body[-1].loc))