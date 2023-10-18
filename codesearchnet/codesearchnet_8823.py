def delete_roles(apps, schema_editor):
    """Delete the enterprise roles."""
    EnterpriseFeatureRole = apps.get_model('enterprise', 'EnterpriseFeatureRole')
    EnterpriseFeatureRole.objects.filter(
        name__in=[ENTERPRISE_CATALOG_ADMIN_ROLE, ENTERPRISE_DASHBOARD_ADMIN_ROLE, ENTERPRISE_ENROLLMENT_API_ADMIN_ROLE]
    ).delete()