def clean(self):
        """
        Clean form fields prior to database entry.

        In this case, the major cleaning operation is substituting a None value for a blank
        value in the Catalog field.
        """
        cleaned_data = super(EnterpriseCustomerAdminForm, self).clean()
        if 'catalog' in cleaned_data and not cleaned_data['catalog']:
            cleaned_data['catalog'] = None
        return cleaned_data