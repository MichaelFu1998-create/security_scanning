def p_open_mixin(self, p):
        """ open_mixin                : identifier t_popen mixin_args_list t_pclose brace_open
                                      | identifier t_popen mixin_args_list t_pclose mixin_guard brace_open
        """
        p[1].parse(self.scope)
        self.scope.current = p[1]
        p[0] = [p[1], p[3]]
        if len(p) > 6:
            p[0].append(p[5])
        else:
            p[0].append(None)