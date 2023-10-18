def _inactivate_organization_course_relationship(relationship):  # pylint: disable=invalid-name
    """
    Inactivates an active organization-course relationship
    """
    relationship = internal.OrganizationCourse.objects.get(
        id=relationship.id,
        active=True
    )
    _inactivate_record(relationship)