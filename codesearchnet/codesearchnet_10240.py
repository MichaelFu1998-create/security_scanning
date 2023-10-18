def fetch_course_organizations(course_key):
    """
    Retrieves the organizations linked to the specified course
    """
    queryset = internal.OrganizationCourse.objects.filter(
        course_id=text_type(course_key),
        active=True
    ).select_related('organization')
    return [serializers.serialize_organization_with_course(organization) for organization in queryset]