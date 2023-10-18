def p_extr_lic_text_1(self, p):
        """extr_lic_text : LICS_TEXT TEXT"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.set_lic_text(self.document, value)
        except OrderError:
            self.order_error('ExtractedText', 'LicenseID', p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('ExtractedText', p.lineno(1))