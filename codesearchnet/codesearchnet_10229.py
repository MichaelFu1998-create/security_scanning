def _activate_organization(organization):
    """
    Activates an inactivated (soft-deleted) organization as well as any inactive relationships
    """
    [_activate_organization_course_relationship(record) for record
     in internal.OrganizationCourse.objects.filter(organization_id=organization.id, active=False)]

    [_activate_record(record) for record
     in internal.Organization.objects.filter(id=organization.id, active=False)]