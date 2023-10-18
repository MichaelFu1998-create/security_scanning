def p_doc_name_1(self, p):
        """doc_name : DOC_NAME LINE"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.set_doc_name(self.document, value)
        except CardinalityError:
            self.more_than_one_error('DocumentName', p.lineno(1))