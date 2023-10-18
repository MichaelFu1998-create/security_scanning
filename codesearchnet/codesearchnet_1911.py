def import_as_name(self, name_tok, as_name_opt):
        """import_as_name: NAME ['as' NAME]"""
        asname_name = asname_loc = as_loc = None
        loc = name_tok.loc
        if as_name_opt:
            as_loc, asname = as_name_opt
            asname_name = asname.value
            asname_loc = asname.loc
            loc = loc.join(asname.loc)
        return ast.alias(name=name_tok.value, asname=asname_name,
                         loc=loc, name_loc=name_tok.loc, as_loc=as_loc, asname_loc=asname_loc)