def p_spdx_version_1(self, p):
        """spdx_version : DOC_VERSION LINE"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.set_doc_version(self.document, value)
        except CardinalityError:
            self.more_than_one_error('SPDXVersion', p.lineno(1))
        except SPDXValueError:
            self.error = True
            msg = ERROR_MESSAGES['DOC_VERSION_VALUE'].format(p[2], p.lineno(1))
            self.logger.log(msg)