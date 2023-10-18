def p_ident_parts_aux(self, p):
        """ ident_parts               : ident_parts ident_part
                                      | ident_parts filter_group
        """
        if isinstance(p[2], list):
            p[1].extend(p[2])
        else:
            p[1].append(p[2])
        p[0] = p[1]