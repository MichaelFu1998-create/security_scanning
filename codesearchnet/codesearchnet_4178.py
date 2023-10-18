def p_file_dep_1(self, p):
        """file_dep : FILE_DEP LINE"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.add_file_dep(self.document, value)
        except OrderError:
            self.order_error('FileDependency', 'FileName', p.lineno(1))