def get_enterprise_customer_from_catalog_id(catalog_id):
    """
    Get the enterprise customer id given an enterprise customer catalog id.
    """
    try:
        return str(EnterpriseCustomerCatalog.objects.get(pk=catalog_id).enterprise_customer.uuid)
    except EnterpriseCustomerCatalog.DoesNotExist:
        return None