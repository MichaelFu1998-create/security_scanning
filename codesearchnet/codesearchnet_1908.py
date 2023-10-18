def raise_stmt__30(self, raise_loc, exc_opt):
        """(3.0-) raise_stmt: 'raise' [test ['from' test]]"""
        exc = from_loc = cause = None
        loc = raise_loc
        if exc_opt:
            exc, cause_opt = exc_opt
            loc = loc.join(exc.loc)
            if cause_opt:
                from_loc, cause = cause_opt
                loc = loc.join(cause.loc)
        return ast.Raise(exc=exc, inst=None, tback=None, cause=cause,
                         keyword_loc=raise_loc, from_loc=from_loc, loc=loc)