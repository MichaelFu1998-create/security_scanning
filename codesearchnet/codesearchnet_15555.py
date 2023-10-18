def p_statement_aux(self, p):
        """ statement            : css_charset t_ws css_string t_semicolon
                                 | css_namespace t_ws css_string t_semicolon
        """
        p[0] = Statement(list(p)[1:], p.lineno(1))
        p[0].parse(None)