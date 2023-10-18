def p_pkg_cr_text_value_1(self, p):
        """pkg_cr_text_value : TEXT"""
        if six.PY2:
            p[0] = p[1].decode(encoding='utf-8')
        else:
            p[0] = p[1]