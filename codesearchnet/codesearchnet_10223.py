def _validate_organization_data(organization_data):
    """ Validation helper """
    if not validators.organization_data_is_valid(organization_data):
        exceptions.raise_exception(
            "Organization",
            organization_data,
            exceptions.InvalidOrganizationException
        )