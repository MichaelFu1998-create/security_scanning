def yield_expr__33(self, yield_loc, arg):
        """(3.3-) yield_expr: 'yield' [yield_arg]"""
        if isinstance(arg, ast.YieldFrom):
            arg.yield_loc = yield_loc
            arg.loc = arg.loc.join(arg.yield_loc)
            return arg
        elif arg is not None:
            return ast.Yield(value=arg,
                             yield_loc=yield_loc, loc=yield_loc.join(arg.loc))
        else:
            return ast.Yield(value=None,
                             yield_loc=yield_loc, loc=yield_loc)