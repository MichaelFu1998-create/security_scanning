def p_statement_namespace(self, p):
        """ statement            : css_namespace t_ws word css_string t_semicolon
        """
        p[0] = Statement(list(p)[1:], p.lineno(1))
        p[0].parse(None)