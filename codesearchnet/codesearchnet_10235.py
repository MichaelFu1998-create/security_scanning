def fetch_organization(organization_id):
    """
    Retrieves a specific organization from app/local state
    Returns a dictionary representation of the object
    """
    organization = {'id': organization_id}
    if not organization_id:
        exceptions.raise_exception("organization", organization, exceptions.InvalidOrganizationException)
    organizations = serializers.serialize_organizations(
        internal.Organization.objects.filter(id=organization_id, active=True)
    )
    if not organizations:
        exceptions.raise_exception("organization", organization, exceptions.InvalidOrganizationException)
    return organizations[0]