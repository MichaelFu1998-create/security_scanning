def p_file_type_1(self, p):
        """file_type : FILE_TYPE file_type_value"""
        try:
            self.builder.set_file_type(self.document, p[2])
        except OrderError:
            self.order_error('FileType', 'FileName', p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('FileType', p.lineno(1))