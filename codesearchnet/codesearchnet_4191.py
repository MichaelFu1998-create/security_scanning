def p_file_conc_1(self, p):
        """file_conc : FILE_LICS_CONC conc_license"""
        try:
            self.builder.set_concluded_license(self.document, p[2])
        except SPDXValueError:
            self.error = True
            msg = ERROR_MESSAGES['FILE_LICS_CONC_VALUE'].format(p.lineno(1))
            self.logger.log(msg)
        except OrderError:
            self.order_error('LicenseConcluded', 'FileName', p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('LicenseConcluded', p.lineno(1))