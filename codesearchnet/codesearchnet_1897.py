def decorator(self, at_loc, idents, call_opt, newline_loc):
        """decorator: '@' dotted_name [ '(' [arglist] ')' ] NEWLINE"""
        root = idents[0]
        dec_loc = root.loc
        expr = ast.Name(id=root.value, ctx=None, loc=root.loc)
        for ident in idents[1:]:
          dot_loc = ident.loc.begin()
          dot_loc.begin_pos -= 1
          dec_loc = dec_loc.join(ident.loc)
          expr = ast.Attribute(value=expr, attr=ident.value, ctx=None,
                               loc=expr.loc.join(ident.loc),
                               attr_loc=ident.loc, dot_loc=dot_loc)

        if call_opt:
            call_opt.func = expr
            call_opt.loc = dec_loc.join(call_opt.loc)
            expr = call_opt
        return at_loc, expr