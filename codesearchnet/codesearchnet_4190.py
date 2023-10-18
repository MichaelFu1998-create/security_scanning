def p_file_chksum_1(self, p):
        """file_chksum : FILE_CHKSUM CHKSUM"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.set_file_chksum(self.document, value)
        except OrderError:
            self.order_error('FileChecksum', 'FileName', p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('FileChecksum', p.lineno(1))