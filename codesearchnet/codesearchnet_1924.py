def with_item(self, context, as_opt):
        """(2.7, 3.1-) with_item: test ['as' expr]"""
        if as_opt:
            as_loc, optional_vars = as_opt
            return ast.withitem(context_expr=context, optional_vars=optional_vars,
                                as_loc=as_loc, loc=context.loc.join(optional_vars.loc))
        else:
            return ast.withitem(context_expr=context, optional_vars=None,
                                as_loc=None, loc=context.loc)