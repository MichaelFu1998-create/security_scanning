def p_pkg_home_1(self, p):
        """pkg_home : PKG_HOME pkg_home_value"""
        try:
            self.builder.set_pkg_down_location(self.document, p[2])
        except OrderError:
            self.order_error('PackageHomePage', 'PackageName', p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('PackageHomePage', p.lineno(1))