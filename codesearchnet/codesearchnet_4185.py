def p_conc_license_3(self, p):
        """conc_license : LINE"""
        if six.PY2:
            value = p[1].decode(encoding='utf-8')
        else:
            value = p[1]
        ref_re = re.compile('LicenseRef-.+', re.UNICODE)
        if (p[1] in config.LICENSE_MAP.keys()) or (ref_re.match(p[1]) is not None):
            p[0] = document.License.from_identifier(value)
        else:
            p[0] = self.license_list_parser.parse(value)