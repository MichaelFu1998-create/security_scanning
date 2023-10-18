def update_organization(organization):
    """
    Updates an existing organization in app/local state
    Returns a dictionary representation of the object
    """
    organization_obj = serializers.deserialize_organization(organization)
    try:
        organization = internal.Organization.objects.get(id=organization_obj.id)
        organization.name = organization_obj.name
        organization.short_name = organization_obj.short_name
        organization.description = organization_obj.description
        organization.logo = organization_obj.logo
        organization.active = organization_obj.active
    except internal.Organization.DoesNotExist:
        exceptions.raise_exception("organization", organization, exceptions.InvalidOrganizationException)
    return serializers.serialize_organization(organization)