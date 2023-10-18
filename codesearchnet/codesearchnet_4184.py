def p_file_lics_info_1(self, p):
        """file_lics_info : FILE_LICS_INFO file_lic_info_value"""
        try:
            self.builder.set_file_license_in_file(self.document, p[2])
        except OrderError:
            self.order_error('LicenseInfoInFile', 'FileName', p.lineno(1))
        except SPDXValueError:
            self.error = True
            msg = ERROR_MESSAGES['FILE_LICS_INFO_VALUE'].format(p.lineno(1))
            self.logger.log(msg)