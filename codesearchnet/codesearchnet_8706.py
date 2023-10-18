def get_catalog_options(self):
        """
        Retrieve a list of catalog ID and name pairs.

        Once retrieved, these name pairs can be used directly as a value
        for the `choices` argument to a ChoiceField.
        """
        # TODO: We will remove the discovery service catalog implementation
        # once we have fully migrated customer's to EnterpriseCustomerCatalogs.
        # For now, this code will prevent an admin from creating a new
        # EnterpriseCustomer with a discovery service catalog. They will have to first
        # save the EnterpriseCustomer admin form and then edit the EnterpriseCustomer
        # to add a discovery service catalog.
        if hasattr(self.instance, 'site'):
            catalog_api = CourseCatalogApiClient(self.user, self.instance.site)
        else:
            catalog_api = CourseCatalogApiClient(self.user)
        catalogs = catalog_api.get_all_catalogs()
        # order catalogs by name.
        catalogs = sorted(catalogs, key=lambda catalog: catalog.get('name', '').lower())

        return BLANK_CHOICE_DASH + [
            (catalog['id'], catalog['name'],)
            for catalog in catalogs
        ]