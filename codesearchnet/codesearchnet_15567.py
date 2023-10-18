def p_variable_decl(self, p):
        """ variable_decl            : variable t_colon style_list t_semicolon
        """
        p[0] = Variable(list(p)[1:-1], p.lineno(4))
        p[0].parse(self.scope)