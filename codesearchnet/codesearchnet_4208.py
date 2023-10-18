def p_package_name(self, p):
        """package_name : PKG_NAME LINE"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.create_package(self.document, value)
        except CardinalityError:
            self.more_than_one_error('PackageName', p.lineno(1))