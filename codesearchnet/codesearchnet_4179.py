def p_file_contrib_1(self, p):
        """file_contrib : FILE_CONTRIB LINE"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.add_file_contribution(self.document, value)
        except OrderError:
            self.order_error('FileContributor', 'FileName', p.lineno(1))