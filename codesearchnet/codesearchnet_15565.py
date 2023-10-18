def p_call_mixin(self, p):
        """ call_mixin                : identifier t_popen mixin_args_list t_pclose t_semicolon
        """
        p[1].parse(None)
        p[0] = Deferred(p[1], p[3], p.lineno(4))