def p_extr_lic_id_1(self, p):
        """extr_lic_id : LICS_ID LINE"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.set_lic_id(self.document, value)
        except SPDXValueError:
            self.error = True
            msg = ERROR_MESSAGES['LICS_ID_VALUE'].format(p.lineno(1))
            self.logger.log(msg)