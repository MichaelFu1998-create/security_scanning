def p_unit_list(self, p):
        """ unit_list                : unit_list unit
                                     | unit
        """
        if isinstance(p[1], list):
            if len(p) >= 3:
                if isinstance(p[2], list):
                    p[1].extend(p[2])
                else:
                    p[1].append(p[2])
        else:
            p[1] = [p[1]]
        p[0] = p[1]