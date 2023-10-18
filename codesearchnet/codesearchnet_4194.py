def p_pkg_summary_1(self, p):
        """pkg_summary : PKG_SUM TEXT"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.set_pkg_summary(self.document, value)
        except OrderError:
            self.order_error('PackageSummary', 'PackageFileName', p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('PackageSummary', p.lineno(1))