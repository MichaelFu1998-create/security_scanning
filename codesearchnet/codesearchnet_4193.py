def p_pkg_desc_1(self, p):
        """pkg_desc : PKG_DESC TEXT"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.set_pkg_desc(self.document, value)
        except CardinalityError:
            self.more_than_one_error('PackageDescription', p.lineno(1))
        except OrderError:
            self.order_error('PackageDescription', 'PackageFileName', p.lineno(1))