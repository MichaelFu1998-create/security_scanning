def get_clear_catalog_id_action(description=None):
    """
    Return the action method to clear the catalog ID for a EnterpriseCustomer.
    """
    description = description or _("Unlink selected objects from existing course catalogs")

    def clear_catalog_id(modeladmin, request, queryset):  # pylint: disable=unused-argument
        """
        Clear the catalog ID for a selected EnterpriseCustomer.
        """
        queryset.update(catalog=None)
    clear_catalog_id.short_description = description
    return clear_catalog_id