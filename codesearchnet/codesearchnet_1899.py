def funcdef__26(self, def_loc, ident_tok, args, colon_loc, suite):
        """(2.6, 2.7) funcdef: 'def' NAME parameters ':' suite"""
        return ast.FunctionDef(name=ident_tok.value, args=args, returns=None,
                               body=suite, decorator_list=[],
                               at_locs=[], keyword_loc=def_loc, name_loc=ident_tok.loc,
                               colon_loc=colon_loc, arrow_loc=None,
                               loc=def_loc.join(suite[-1].loc))