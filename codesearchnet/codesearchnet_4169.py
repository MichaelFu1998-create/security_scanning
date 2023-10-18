def p_lic_comment_1(self, p):
        """lic_comment : LICS_COMMENT TEXT"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.set_lic_comment(self.document, value)
        except OrderError:
            self.order_error('LicenseComment', 'LicenseID', p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('LicenseComment', p.lineno(1))