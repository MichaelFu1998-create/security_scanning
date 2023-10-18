def p_pkg_file_name(self, p):
        """pkg_file_name : PKG_FILE_NAME LINE"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.set_pkg_file_name(self.document, value)
        except OrderError:
            self.order_error('PackageFileName', 'PackageName', p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('PackageFileName', p.lineno(1))