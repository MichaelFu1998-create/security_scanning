def p_lic_xref_1(self, p):
        """lic_xref : LICS_CRS_REF LINE"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.add_lic_xref(self.document, value)
        except OrderError:
            self.order_error('LicenseCrossReference', 'LicenseName', p.lineno(1))