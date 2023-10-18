def p_pkg_lic_comment_1(self, p):
        """pkg_lic_comment : PKG_LICS_COMMENT TEXT"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.set_pkg_license_comment(self.document, value)
        except OrderError:
            self.order_error('PackageLicenseComments', 'PackageFileName', p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('PackageLicenseComments', p.lineno(1))