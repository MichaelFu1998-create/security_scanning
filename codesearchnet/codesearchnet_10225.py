def remove_organization_course(organization, course_key):
    """
    Removes the specfied course from the specified organization
    """
    _validate_organization_data(organization)
    _validate_course_key(course_key)
    return data.delete_organization_course(course_key=course_key, organization=organization)