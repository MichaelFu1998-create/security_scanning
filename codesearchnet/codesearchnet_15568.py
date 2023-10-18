def p_property_decl(self, p):
        """ property_decl           : prop_open style_list t_semicolon
                                    | prop_open style_list css_important t_semicolon
                                    | prop_open empty t_semicolon
        """
        l = len(p)
        p[0] = Property(list(p)[1:-1], p.lineno(l - 1))