def p_created_1(self, p):
        """created : CREATED DATE"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.set_created_date(self.document, value)
        except CardinalityError:
            self.more_than_one_error('Created', p.lineno(1))