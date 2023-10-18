def except_clause(self, except_loc, exc_opt):
        """
        (2.6, 2.7) except_clause: 'except' [test [('as' | ',') test]]
        (3.0-) except_clause: 'except' [test ['as' NAME]]
        """
        type_ = name = as_loc = name_loc = None
        loc = except_loc
        if exc_opt:
            type_, name_opt = exc_opt
            loc = loc.join(type_.loc)
            if name_opt:
                as_loc, name_tok, name_node = name_opt
                if name_tok:
                    name = name_tok.value
                    name_loc = name_tok.loc
                else:
                    name = name_node
                    name_loc = name_node.loc
                loc = loc.join(name_loc)
        return ast.ExceptHandler(type=type_, name=name,
                                 except_loc=except_loc, as_loc=as_loc, name_loc=name_loc,
                                 loc=loc)