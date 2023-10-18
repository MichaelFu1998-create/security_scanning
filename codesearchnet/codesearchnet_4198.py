def p_pkg_lic_ff_1(self, p):
        """pkg_lic_ff : PKG_LICS_FFILE pkg_lic_ff_value"""
        try:
            self.builder.set_pkg_license_from_file(self.document, p[2])
        except OrderError:
            self.order_error('PackageLicenseInfoFromFiles', 'PackageName', p.lineno(1))
        except SPDXValueError:
            self.error = True
            msg = ERROR_MESSAGES['PKG_LIC_FFILE_VALUE'].format(p.lineno(1))
            self.logger.log(msg)