def p_package_version_1(self, p):
        """package_version : PKG_VERSION LINE"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.set_pkg_vers(self.document, value)
        except OrderError:
            self.order_error('PackageVersion', 'PackageName', p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('PackageVersion', p.lineno(1))