def _inactivate_organization(organization):
    """
    Inactivates an activated organization as well as any active relationships
    """
    [_inactivate_organization_course_relationship(record) for record
     in internal.OrganizationCourse.objects.filter(organization_id=organization.id, active=True)]

    [_inactivate_record(record) for record
     in internal.Organization.objects.filter(id=organization.id, active=True)]