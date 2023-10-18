def create_roles(apps, schema_editor):
    """Create the enterprise roles if they do not already exist."""
    EnterpriseFeatureRole = apps.get_model('enterprise', 'EnterpriseFeatureRole')
    EnterpriseFeatureRole.objects.update_or_create(name=ENTERPRISE_CATALOG_ADMIN_ROLE)
    EnterpriseFeatureRole.objects.update_or_create(name=ENTERPRISE_DASHBOARD_ADMIN_ROLE)
    EnterpriseFeatureRole.objects.update_or_create(name=ENTERPRISE_ENROLLMENT_API_ADMIN_ROLE)