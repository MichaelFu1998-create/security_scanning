def p_file_name_1(self, p):
        """file_name : FILE_NAME LINE"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.set_file_name(self.document, value)
        except OrderError:
            self.order_error('FileName', 'PackageName', p.lineno(1))