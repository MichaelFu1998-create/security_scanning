def p_file_lics_comment_1(self, p):
        """file_lics_comment : FILE_LICS_COMMENT TEXT"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.set_file_license_comment(self.document, value)
        except OrderError:
            self.order_error('LicenseComments', 'FileName', p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('LicenseComments', p.lineno(1))