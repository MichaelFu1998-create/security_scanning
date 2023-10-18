def p_file_cr_value_1(self, p):
        """file_cr_value : TEXT"""
        if six.PY2:
            p[0] = p[1].decode(encoding='utf-8')
        else:
            p[0] = p[1]