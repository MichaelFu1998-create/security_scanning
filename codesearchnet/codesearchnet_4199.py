def p_pkg_lic_ff_value_3(self, p):
        """pkg_lic_ff_value : LINE"""
        if six.PY2:
            value = p[1].decode(encoding='utf-8')
        else:
            value = p[1]
        p[0] = document.License.from_identifier(value)