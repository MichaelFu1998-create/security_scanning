def _activate_organization_course_relationship(relationship):  # pylint: disable=invalid-name
    """
    Activates an inactive organization-course relationship
    """
    # If the relationship doesn't exist or the organization isn't active we'll want to raise an error
    relationship = internal.OrganizationCourse.objects.get(
        id=relationship.id,
        active=False,
        organization__active=True
    )
    _activate_record(relationship)