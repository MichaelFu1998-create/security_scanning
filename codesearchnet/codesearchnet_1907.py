def raise_stmt__26(self, raise_loc, type_opt):
        """(2.6, 2.7) raise_stmt: 'raise' [test [',' test [',' test]]]"""
        type_ = inst = tback = None
        loc = raise_loc
        if type_opt:
            type_, inst_opt = type_opt
            loc = loc.join(type_.loc)
            if inst_opt:
                _, inst, tback = inst_opt
                loc = loc.join(inst.loc)
                if tback:
                    loc = loc.join(tback.loc)
        return ast.Raise(exc=type_, inst=inst, tback=tback, cause=None,
                         keyword_loc=raise_loc, from_loc=None, loc=loc)