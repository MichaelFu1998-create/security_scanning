def clean(self):
        """
        Override of clean method to perform additional validation
        """
        cleaned_data = super(EnterpriseCustomerReportingConfigAdminForm, self).clean()
        report_customer = cleaned_data.get('enterprise_customer')

        # Check that any selected catalogs are tied to the selected enterprise.
        invalid_catalogs = [
            '{} ({})'.format(catalog.title, catalog.uuid)
            for catalog in cleaned_data.get('enterprise_customer_catalogs')
            if catalog.enterprise_customer != report_customer
        ]

        if invalid_catalogs:
            message = _(
                'These catalogs for reporting do not match enterprise'
                'customer {enterprise_customer}: {invalid_catalogs}',
            ).format(
                enterprise_customer=report_customer,
                invalid_catalogs=invalid_catalogs,
            )
            self.add_error('enterprise_customer_catalogs', message)