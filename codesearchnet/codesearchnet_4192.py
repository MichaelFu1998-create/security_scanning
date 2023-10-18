def p_file_type_value(self, p):
        """file_type_value : OTHER
                           | SOURCE
                           | ARCHIVE
                           | BINARY
        """
        if six.PY2:
            p[0] = p[1].decode(encoding='utf-8')
        else:
            p[0] = p[1]