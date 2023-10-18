def p_pkg_home_2(self, p):
        """pkg_home : PKG_HOME error"""
        self.error = True
        msg = ERROR_MESSAGES['PKG_HOME_VALUE']
        self.logger.log(msg)