def p_doc_comment_1(self, p):
        """doc_comment : DOC_COMMENT TEXT"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.set_doc_comment(self.document, value)
        except CardinalityError:
            self.more_than_one_error('DocumentComment', p.lineno(1))