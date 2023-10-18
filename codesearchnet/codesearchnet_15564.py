def p_mixin_guard_cond_list_aux(self, p):
        """ mixin_guard_cond_list    : mixin_guard_cond_list t_comma mixin_guard_cond
                                     | mixin_guard_cond_list less_and mixin_guard_cond
        """
        p[1].append(p[2])
        p[1].append(p[3])
        p[0] = p[1]