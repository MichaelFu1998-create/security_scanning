def p_file_notice_1(self, p):
        """file_notice : FILE_NOTICE TEXT"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.set_file_notice(self.document, value)
        except OrderError:
            self.order_error('FileNotice', 'FileName', p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('FileNotice', p.lineno(1))