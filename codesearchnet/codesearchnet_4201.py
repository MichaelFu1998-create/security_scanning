def p_pkg_chksum_1(self, p):
        """pkg_chksum : PKG_CHKSUM CHKSUM"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.set_pkg_chk_sum(self.document, value)
        except OrderError:
            self.order_error('PackageChecksum', 'PackageFileName', p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('PackageChecksum', p.lineno(1))