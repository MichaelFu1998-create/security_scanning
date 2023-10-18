def p_ident_parts(self, p):
        """ ident_parts               : ident_part
                                      | selector
                                      | filter_group
        """
        if not isinstance(p[1], list):
            p[1] = [p[1]]
        p[0] = p[1]