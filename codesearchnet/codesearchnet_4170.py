def p_extr_lic_name_1(self, p):
        """extr_lic_name : LICS_NAME extr_lic_name_value"""
        try:
            self.builder.set_lic_name(self.document, p[2])
        except OrderError:
            self.order_error('LicenseName', 'LicenseID', p.lineno(1))
        except CardinalityError:
            self.more_than_one_error('LicenseName', p.lineno(1))