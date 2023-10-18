def import_from(self, from_loc, module_name, import_loc, names):
        """
        (2.6, 2.7)
        import_from: ('from' ('.'* dotted_name | '.'+)
                      'import' ('*' | '(' import_as_names ')' | import_as_names))
        (3.0-)
        # note below: the ('.' | '...') is necessary because '...' is tokenized as ELLIPSIS
        import_from: ('from' (('.' | '...')* dotted_name | ('.' | '...')+)
                      'import' ('*' | '(' import_as_names ')' | import_as_names))
        """
        (dots_loc, dots_count), dotted_name_opt = module_name
        module_loc = module = None
        if dotted_name_opt:
            module_loc, module = dotted_name_opt
        lparen_loc, names, rparen_loc = names
        loc = from_loc.join(names[-1].loc)
        if rparen_loc:
            loc = loc.join(rparen_loc)

        if module == "__future__":
            self.add_flags([x.name for x in names])

        return ast.ImportFrom(names=names, module=module, level=dots_count,
                              keyword_loc=from_loc, dots_loc=dots_loc, module_loc=module_loc,
                              import_loc=import_loc, lparen_loc=lparen_loc, rparen_loc=rparen_loc,
                              loc=loc)