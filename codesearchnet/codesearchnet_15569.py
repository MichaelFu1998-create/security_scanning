def p_identifier_list_aux(self, p):
        """ identifier_list           : identifier_list t_comma identifier_group
        """
        p[1].extend([p[2]])
        p[1].extend(p[3])
        p[0] = p[1]