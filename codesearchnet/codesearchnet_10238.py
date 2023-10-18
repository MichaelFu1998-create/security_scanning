def delete_organization_course(organization, course_key):
    """
    Removes an existing organization-course relationship from app/local state
    No response currently defined for this operation
    """
    try:
        relationship = internal.OrganizationCourse.objects.get(
            organization=organization['id'],
            course_id=text_type(course_key),
            active=True,
        )
        _inactivate_organization_course_relationship(relationship)
    except internal.OrganizationCourse.DoesNotExist:
        # If we're being asked to delete an organization-course link
        # that does not exist in the database then our work is done
        pass