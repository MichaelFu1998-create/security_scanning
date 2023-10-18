def p_file_comment_1(self, p):
        """file_comment : FILE_COMMENT TEXT"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.set_file_comment(self.document, value)
        except OrderError:
            self.order_error('FileComment', 'FileName', p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('FileComment', p.lineno(1))