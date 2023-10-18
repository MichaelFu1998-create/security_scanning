def create_roles(apps, schema_editor):
    """Create the enterprise roles if they do not already exist."""
    SystemWideEnterpriseRole = apps.get_model('enterprise', 'SystemWideEnterpriseRole')
    SystemWideEnterpriseRole.objects.update_or_create(name=ENTERPRISE_ADMIN_ROLE)
    SystemWideEnterpriseRole.objects.update_or_create(name=ENTERPRISE_LEARNER_ROLE)