def create_organization(organization):
    """
    Inserts a new organization into app/local state given the following dictionary:
    {
        'name': string,
        'description': string
    }
    Returns an updated dictionary including a new 'id': integer field/value
    """
    # Trust, but verify...
    if not organization.get('name'):
        exceptions.raise_exception("organization", organization, exceptions.InvalidOrganizationException)
    organization_obj = serializers.deserialize_organization(organization)
    try:
        organization = internal.Organization.objects.get(
            name=organization_obj.name,
        )
        # If the organization exists, but was inactivated, we can simply turn it back on
        if not organization.active:
            _activate_organization(organization_obj)
    except internal.Organization.DoesNotExist:
        organization = internal.Organization.objects.create(
            name=organization_obj.name,
            short_name=organization_obj.short_name,
            description=organization_obj.description,
            logo=organization_obj.logo,
            active=True
        )
    return serializers.serialize_organization(organization)