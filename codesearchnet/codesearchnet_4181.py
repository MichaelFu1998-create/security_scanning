def p_file_cr_text_1(self, p):
        """file_cr_text : FILE_CR_TEXT file_cr_value"""
        try:
            self.builder.set_file_copyright(self.document, p[2])
        except OrderError:
            self.order_error('FileCopyrightText', 'FileName', p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('FileCopyrightText', p.lineno(1))