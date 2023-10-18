def dotted_as_name(self, dotted_name, as_name_opt):
        """dotted_as_name: dotted_name ['as' NAME]"""
        asname_name = asname_loc = as_loc = None
        dotted_name_loc, dotted_name_name = dotted_name
        loc = dotted_name_loc
        if as_name_opt:
            as_loc, asname = as_name_opt
            asname_name = asname.value
            asname_loc = asname.loc
            loc = loc.join(asname.loc)
        return ast.alias(name=dotted_name_name, asname=asname_name,
                         loc=loc, name_loc=dotted_name_loc, as_loc=as_loc, asname_loc=asname_loc)