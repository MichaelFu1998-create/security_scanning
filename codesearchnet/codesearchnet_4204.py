def p_pkg_home_value_1(self, p):
        """pkg_home_value : LINE"""
        if six.PY2:
            p[0] = p[1].decode(encoding='utf-8')
        else:
            p[0] = p[1]