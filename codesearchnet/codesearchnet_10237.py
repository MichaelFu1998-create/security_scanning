def create_organization_course(organization, course_key):
    """
    Inserts a new organization-course relationship into app/local state
    No response currently defined for this operation
    """
    organization_obj = serializers.deserialize_organization(organization)
    try:
        relationship = internal.OrganizationCourse.objects.get(
            organization=organization_obj,
            course_id=text_type(course_key)
        )
        # If the relationship exists, but was inactivated, we can simply turn it back on
        if not relationship.active:
            _activate_organization_course_relationship(relationship)
    except internal.OrganizationCourse.DoesNotExist:
        relationship = internal.OrganizationCourse.objects.create(
            organization=organization_obj,
            course_id=text_type(course_key),
            active=True
        )