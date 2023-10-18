def fetch_organization_by_short_name(organization_short_name):
    """
    Retrieves a specific organization from app/local state by short name
    Returns a dictionary representation of the object
    """
    organization = {'short_name': organization_short_name}
    if not organization_short_name:
        exceptions.raise_exception("organization", organization, exceptions.InvalidOrganizationException)
    organizations = serializers.serialize_organizations(internal.Organization.objects.filter(
        active=True, short_name=organization_short_name
    ))
    if not organizations:
        exceptions.raise_exception("organization", organization, exceptions.InvalidOrganizationException)
    return organizations[0]