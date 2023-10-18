def p_pkg_cr_text_1(self, p):
        """pkg_cr_text : PKG_CPY_TEXT pkg_cr_text_value"""
        try:
            self.builder.set_pkg_cr_text(self.document, p[2])
        except OrderError:
            self.order_error('PackageCopyrightText', 'PackageFileName', p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('PackageCopyrightText', p.lineno(1))