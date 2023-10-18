def add_organization_course(organization_data, course_key):
    """
    Adds a organization-course link to the system
    """
    _validate_course_key(course_key)
    _validate_organization_data(organization_data)
    data.create_organization_course(
        organization=organization_data,
        course_key=course_key
    )