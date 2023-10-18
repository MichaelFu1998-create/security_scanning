def p_extr_lic_name_value_1(self, p):
        """extr_lic_name_value : LINE"""
        if six.PY2:
            p[0] = p[1].decode(encoding='utf-8')
        else:
            p[0] = p[1]