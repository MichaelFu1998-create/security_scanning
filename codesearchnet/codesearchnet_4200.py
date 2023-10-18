def p_pkg_src_info_1(self, p):
        """pkg_src_info : PKG_SRC_INFO TEXT"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.set_pkg_source_info(self.document, value)
        except CardinalityError:
            self.more_than_one_error('PackageSourceInfo', p.lineno(1))
        except OrderError:
            self.order_error('PackageSourceInfo', 'PackageFileName', p.lineno(1))