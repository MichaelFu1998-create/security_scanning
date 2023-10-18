def fetch_organization_courses(organization):
    """
    Retrieves the set of courses currently linked to the specified organization
    """
    organization_obj = serializers.deserialize_organization(organization)
    queryset = internal.OrganizationCourse.objects.filter(
        organization=organization_obj,
        active=True
    ).select_related('organization')
    return [serializers.serialize_organization_with_course(organization) for organization in queryset]